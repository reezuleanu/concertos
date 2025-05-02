import React from 'react'
import "./event_settings_actions.css"
import Programmer from '../components/programmer'


const EventSettingsActions = () => {
  return (
    <div className='content'>
    <div className='filler'><text>This is the visual programmer. Here, you can program device commands and when they should be executed, completely from the interface.</text></div>
    <Programmer/>
</div>
  )
}

export default EventSettingsActions

