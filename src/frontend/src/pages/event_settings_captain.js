import React from 'react'
import "./event_settings_actions.css"
import Captain from '../components/captain'


const EventSettingsCaptain = () => {
  return (
    <div className='content'>
        <div className='filler'><text>This is the Captain's Cabin. Here, you have access to all the buttons for the Captain Triggers.</text></div>
        <Captain/>
    </div>
  )
}

export default EventSettingsCaptain

