import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import "./firmware.css"

const backend = `http://${process.env.REACT_APP_BACKEND_IP}:${process.env.REACT_APP_BACKEND_PORT}`



const FirmwareCard = ({id}) => {

    const [data, setData] = useState({})

    useEffect(()=>{
        const getData = async () => {
            const response = await fetch(`${backend}/firmware/${id}`)
            const d = await response.json()
            setData(d)
        }
        getData()
    },[])


    return (
        <>
            <div className='firmware-card'>
                <h3>{data.name}</h3>
                <h5>{data.version}</h5>
                <p>{data.description}</p>
                <a href={`${backend}/firmware/${id}/download`}>
                    <button>download</button>
                </a>
                
            </div>
        </>
      )

}


const Firmware = () => {
    
    const [firmwares, setFirmwares] = useState([])

    useEffect(()=>{

        const getFirmwares = async () => {
            const response = await fetch(`${backend}/firmware/`)
            const data = await response.json()
            setFirmwares(data)
        }
        getFirmwares()

    }, [])

    return (
    <>
        <div className='firmware'>
            {/* <FirmwareCard id={1} /> */}
        {Object.entries(firmwares).map(([_, id]) => (
            <FirmwareCard id = {id}/>
        ))}
        </div>
    </>
  )
}

export default Firmware
