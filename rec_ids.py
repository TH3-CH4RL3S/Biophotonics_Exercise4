# Using (IDS Camera)

from ids_peak import ids_peak
from ids_peak import ids_peak_ipl_extension
import cv2
import os
import time
import numpy


def main():
    # Parameters
    output_dir = "recorded_frames_COLD_left_HOT_right_final"
    record_duration = 30  # Record for 10 seconds
    frame_rate = 50  # Frames per second

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Initialize library
    ids_peak.Library.Initialize()

    # Create a DeviceManager object
    device_manager = ids_peak.DeviceManager.Instance()

    try:
        # Update the DeviceManager
        device_manager.Update()

        # Check if any devices are available
        if device_manager.Devices().empty():
            print("No device found. Exiting Program.")
            return -1

        # Open the first device
        device = device_manager.Devices()[0].OpenDevice(
            ids_peak.DeviceAccessType_Control)

        # Access the nodemap for camera settings
        remote_nodemap = device.RemoteDevice().NodeMaps()[0]

        # Load default settings
        remote_nodemap.FindNode("UserSetSelector").SetCurrentEntry("Default")
        remote_nodemap.FindNode("UserSetLoad").Execute()
        remote_nodemap.FindNode("UserSetLoad").WaitUntilDone()

        remote_nodemap.FindNode("PixelFormat").SetCurrentEntry("Mono8")
        
        remote_nodemap.FindNode("Gain").SetValue(3)

        # Set exposure and frame rate
        remote_nodemap.FindNode("ExposureTime").SetValue(5500)  # Microseconds
        remote_nodemap.FindNode("ExposureAuto").SetCurrentEntry("Off")
        remote_nodemap.FindNode("Width").SetValue(1000)
        remote_nodemap.FindNode("Height").SetValue(1000)
        remote_nodemap.FindNode("AcquisitionFrameRate").SetValue(frame_rate)

        # Open the data stream
        data_stream = device.DataStreams()[0].OpenDataStream()
        payload_size = remote_nodemap.FindNode("PayloadSize").Value()

        # Allocate buffers
        buffer_count_max = data_stream.NumBuffersAnnouncedMinRequired()
        for _ in range(buffer_count_max):
            buffer = data_stream.AllocAndAnnounceBuffer(payload_size)
            data_stream.QueueBuffer(buffer)

        # Lock parameters during acquisition
        remote_nodemap.FindNode("TLParamsLocked").SetValue(1)

        # Start acquisition
        print("Starting acquisition...")
        data_stream.StartAcquisition()
        remote_nodemap.FindNode("AcquisitionStart").Execute()
        remote_nodemap.FindNode("AcquisitionStart").WaitUntilDone()

        # Record frames
        print("Recording frames...")
        start_time = time.time()
        frame_count = 0

        while time.time() - start_time < record_duration:
            try:
                # Wait for a finished buffer
                buffer = data_stream.WaitForFinishedBuffer(1000)
                img = ids_peak_ipl_extension.BufferToImage(buffer)
#  np_img =  # Convert to NumPy array

                # Save the frame
                cv2.imwrite(f"{output_dir}/frame_{frame_count:04d}.png", img.get_numpy_2D())
                frame_count += 1

                # Requeue the buffer
                data_stream.QueueBuffer(buffer)
            except Exception as e:
                print(f"Exception during frame acquisition: {e}")
                break

        print(f"Recording completed. {frame_count} frames saved to '{output_dir}'.")

        # Stop acquisition
        print("Stopping acquisition...")
        remote_nodemap.FindNode("AcquisitionStop").Execute()
        remote_nodemap.FindNode("AcquisitionStop").WaitUntilDone()
        data_stream.StopAcquisition(ids_peak.AcquisitionStopMode_Default)

        # Clean up buffers
        data_stream.Flush(ids_peak.DataStreamFlushMode_DiscardAll)
        for buffer in data_stream.AnnouncedBuffers():
            data_stream.RevokeBuffer(buffer)

        # Unlock parameters
        remote_nodemap.FindNode("TLParamsLocked").SetValue(0)

    except Exception as e:
        print("EXCEPTION: " + str(e))
        return -2

    finally:
        ids_peak.Library.Close()


if __name__ == "__main__":
    main()
