import React, { useEffect, useState } from 'react'
import Modal from './modal'
import "./modal.css"
import "./devices.css"


const backend = `http://${process.env.REACT_APP_BACKEND_IP}:${process.env.REACT_APP_BACKEND_PORT}`

const DeviceCard = ({id, device_name, device_type, device_address, device_port, onDelete, onSubmit}) => {

    const [data, setData] = useState({id: id, name: device_name,type:device_type, address: device_address, port:device_port})
    const [modalType, setModalType] = useState(null)
    const [props, setProps] = useState()


    const closeModal = () => {
        setModalType(null)
    }
    
    const handleSubmit = (e, data) =>{
        // e.preventDefault()
        // setData(data)
        // closeModal()
        onSubmit(id, data)
    }
    const handleDelete = () => {
        onDelete(id)
    }
    

    const handleClick = () =>{
        // console.log(data)
        setProps({...data, onCancel: closeModal, onSubmit: handleSubmit, onDelete:handleDelete})
        setModalType("device")
    }

    return (
    <>
    <Modal type={modalType} props={props}/>
    <div className='device-card' onClick={handleClick}>
        <h3>{data.name}</h3>
        <text>{data.address}:{data.port}</text>
    </div>
    </>
  )
}


const AdderCard = ({onSubmit}) =>{
    const [modalType, setModalType] = useState(null)
    const [props, setProps] = useState()

    const closeModal = () =>{
        setModalType(null)
    }

    const handleSubmit = (e, new_device) => {
        onSubmit(new_device)
    }

    const handleClick = () => {
        setProps({onCancel: closeModal, onSubmit: handleSubmit, onDelete: closeModal})
        setModalType("device")
    }

    return(
        <>
            <Modal type={modalType} props={props}/>
            <div className="device-adder" onClick={()=>handleClick()}>
                +
            </div>
        </>
    )
}


const Devices = ({event_id}) => {

    const [devices, setDevices] = useState([])

    const getDevices = async() => {
        const request = await fetch(`${backend}/events/${event_id}/devices/hardware/expanded`)
        if(!request.ok){
            return
        }
        const data = await request.json()
        // console.log(data)
        setDevices(data)
    }

    useEffect(()=>{
        getDevices()
    },[])

    const postDevice = async (new_device) =>{
        const request = await fetch(`${backend}/events/${event_id}/devices/hardware`, {
            method:"POST",
            headers:{"content-type":"application/json"},
            body:JSON.stringify(new_device)
        })
        if(!request.ok){
            console.log("Could not create new device " + request.status)
        }
    }

    const updateDevice = async(id, new_device) =>{
        const request = await fetch(`${backend}/events/${event_id}/devices/${id}/`, {
            method:"PUT",
            headers:{
                "content-type": "application/json",
            },
            body: JSON.stringify(new_device),
        })
        if(!request.ok){
            console.log("Could not update device " + id + " error " + request.status)
            return
        }
    }

    const deleteDevice = async(id) => {
        const request = await fetch(`${backend}/events/${event_id}/devices/${id}/`, {
            method:"DELETE",
        })
        if(!request.ok){
            console.log("Could not delete device " + request.status)
            return
        }
    }


    return(
        <div className='devices'>
            {Object.entries(devices).map(([id,props])=>(
                // console.log(id, props)
                <DeviceCard id = {id} device_name = {props.name} device_type={props.type} device_address={props.address} device_port={props.port} onDelete = {deleteDevice} onSubmit = {updateDevice}/>
            ))}
            <AdderCard event_id= {event_id} onSubmit = {postDevice} />
        </div>
    )
}


export default Devices
