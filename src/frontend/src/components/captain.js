import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import "./captain.css"

const backend = `http://${process.env.REACT_APP_BACKEND_IP}:${process.env.REACT_APP_BACKEND_PORT}`


const Captain = () => {
    
    let {eventid} = useParams()
    const [buttons, setButtons] = useState([])

    useEffect(()=>{
        const getButtons = async () =>{
            const response = await fetch(`${backend}/events/${eventid}/actions/captain`)
            if(!response.ok){
                console.log("Could not fetch captain trigger names " + response.status)
            }
            const btns = await response.json()
            setButtons(btns)
        }
        getButtons()
    }, [])
  
    return (
    <>
        <div className='captain'>
        {Object.entries(buttons).map(([_, name])=>(
            <div className='captain-button'>
                <h3>{name}</h3>
                <button onClick={()=>fetch(`${backend}/events/${eventid}/actions/captain/${name}/`, {method:"POST"})}>Trigger</button>
            </div>
            ))}
        </div>
    </>
  )
}

export default Captain
