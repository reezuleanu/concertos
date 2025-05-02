import React from 'react'
import Sidebar from '../components/sidebar'
import EventSettingsActions from './event_settings_actions';
import "./event_settings.css"
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react'
import EventSettingsDevices from './event_settings_devices';
import EventSettingsCaptain from './event_settings_captain';

const backend = `http://${process.env.REACT_APP_BACKEND_IP}:${process.env.REACT_APP_BACKEND_PORT}`

const Settings = () => {
    const [eventName, setEventName] = useState("eventName")

    // get option from url
    let {option} = useParams()
    // console.log(option)

    // get event from url
    let {eventid} = useParams()

    // temp patch
    if(!eventid){
        setEventName("eventName")
    }


    useEffect(() => {
        const getEventName = async() =>{
            const response = await fetch(`${backend}/events/${eventid}`)
            if(!response.ok){
                return
            }
            const event_name = await response.json()
            setEventName(event_name.name)
        }
        getEventName();
    }, [eventid])

  return (
    <div className='settings-header'>
        <h2>{eventName} Settings</h2>
    <div className='settings'>
        <Sidebar option={option} eventName = {eventName}/>
        <div>
            {(()=>{
                switch(option){
                    case "actions":
                        return <EventSettingsActions/>
                    case "devices":
                        return <EventSettingsDevices/>
                    case "captain":
                        return <EventSettingsCaptain/>
                    default:
                        return option
                }
            })()}
        </div>
        
    </div></div>
  )
}

export default Settings
