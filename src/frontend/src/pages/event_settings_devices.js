import React from 'react'
import "./event_settings_devices.css"
import Devices from '../components/devices'
import { useParams } from 'react-router-dom'

const EventSettingsDevices = () => {
  let {eventid} = useParams()
  return (
    <>
    <div className='content'>
        <div className='filler'>
            <text>Here are the current devices for this event and their details. To edit a device, click on its card. To add a new device, hit on the + card.</text>
        </div>
        <Devices event_id={eventid}/>
    </div>
    </>
  )
}

export default EventSettingsDevices
