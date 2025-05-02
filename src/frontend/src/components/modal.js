import React, { useEffect, useState} from 'react'
import "./modal.css"
import ReactDom from 'react-dom'
import { useParams } from 'react-router-dom';

const backend = `http://${process.env.REACT_APP_BACKEND_IP}:${process.env.REACT_APP_BACKEND_PORT}`

// Modal Factory
function Modal({type, props}){
  if(type === null){
    return;
  }

  switch(type){
    case "trigger":
      return TriggerModal(props)
    case "command":
      return CommandModal(props)
    case "action":
      return ActionModal(props)
    case "device":
      return DeviceModal(props)
    default:
      return null;
  }
}

function ActionModal({name, onCancel, onSubmit, onDelete}){
  const [actionName, setActionName] = useState(name)

  const handleSubmit = (e) =>{
    onSubmit(actionName)
  }


  return ReactDom.createPortal(
    <>
    <div className='overlay' onClick={() => onCancel()}></div>
    <div className='modal'>
      <div className='header-div'>
        <text onClick={()=>onCancel()}>&times;</text>
        <h2>Edit Action</h2>
      </div>
      <form onSubmit={handleSubmit}>
      <div>
        <label>Name</label>
        <input required type="text" placeholder='Action Name' value={actionName} onChange={(e)=>setActionName(e.target.value)}></input>
      </div>
      <div className='buttons'>
        <button onClick={()=>(onDelete) ? onDelete() : console.log("No delete function defined")}>Delete</button>
        <button type="submit">Change Name</button>
      </div>
      </form>
    </div>
    </>, document.getElementById("portal")
  )
}



// pop up component for creating/editing a trigger
function TriggerModal({event, parent, getData, onSubmit, onCancel, onDelete}) {
  
  // get trigger data
  const [data, setData] = useState(getData(parent))

  // trigger types
  const [types, setTypes] = useState({"None":"none"})

  // custom variables
  const [variables, setVariables] = useState({"None":"None"})


  // default values
  if(!data.condition){
    data.condition = "="
  }

  if(data.target_value === undefined){
    data.target_value=0
  }

  if(!data.type){
    data.type = "value"
  }


  // get available trigger types from Django
  // TODO hardcode this instead
  const getTypes = async () => {
    try{
      const response = await fetch(`${backend}/actions/triggers`)

      if(!response.ok){
        console.log("Something went wrong, " + response.status)
        return
      }

      const data = await response.json()
      setTypes(data)}
    catch{
      console.log("Could not connect")
    }
  }



  // fetch custom variables for use with value trigger
  const getVariables = async () => {
    try{
      const response = await fetch(`${backend}/events/${event}/actions/variables/global/`)

      if(!response.ok){
        return
      }

      const data = await response.json()
      setVariables(data)
    }
    catch{
      console.log("Could not connect to get variables")
    }
  }

  useEffect(()=>{
    getTypes()
  }, [])

  useEffect(()=>{
    if(!data.type){
      setData({...data, type: Object.entries(types)[0][1]})
    }
    getVariables()
  },[types])

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(data, parent)
  }

  return ReactDom.createPortal(
    <>
    <div className='overlay' onClick={() => onCancel()}></div>
    <div className='modal'>
      <div className='header-div'>
        <text onClick={() => onCancel()}>&times;</text>
        <h2>Edit Trigger</h2>
      </div>
      <form onSubmit={handleSubmit}>
      <div>
        <label>Type</label>
        <select value={data.type} onChange={(e) => setData({...data, type:e.target.value})}>
          {/* <option value={"none"}>None</option> */}
          {Object.entries(types).map(([name, value]) => (
            <option value={value}>
              {name}
            </option>
          ))}
        </select>
      </div>
      {(()=>{
          switch(data.type){
              case "value":
                  return(
                  <>
                  <div>
                    <label>Condition</label>
                    <select value={data.condition} onChange={(e)=>setData({...data, condition:e.target.value})}>
                      <option value = "=">=</option>
                      <option value = ">">{">"}</option>
                      <option value = ">=">{">="}</option>
                      <option value = "<">{"<"}</option>
                      <option value = "<=">{"<="}</option>
                      <option value = "!">!</option>
                    </select>
                  </div>
                  <div>
                    <label>Variable</label>
                    <select required value={(data.variable_name) ? data.variable_name : ""} onChange={(e)=>setData({...data, variable_name:e.target.value})}>
                      <option value="">-</option>
                      {Object.entries(variables).map(([name, value]) => (
                        <option value={value}>
                          {name}
                        </option>
                        ))}
                    </select>
                  </div>
                  <div>
                    <label>Target Value</label>
                    <input required type="number" value={data.target_value} placeholder='Target Value' onChange={(e)=>setData({...data, target_value:e.target.value})}></input>
                  </div>
                  </>)
              case "time":
                data.condition = ">="
                data.variable_name = "TIME"
                return(
                  <>
                  <div>
                    <label>Time in Seconds</label>
                    <input required type="number" value={data.target_value} placeholder='Target Value' onChange={(e)=>setData({...data, target_value:e.target.value})}></input>
                  </div>
                  </>)
              case "date":
                data.variable_name = "DATE"
                return(
                  <>
                  <div>
                    <label>Condition</label>
                    <select value={data.condition} onChange={(e)=>setData({...data, condition:e.target.value})}>
                      <option value = "=">=</option>
                      <option value = ">">{">"}</option>
                      <option value = ">=">{">="}</option>
                      <option value = "<">{"<"}</option>
                      <option value = "<=">{"<="}</option>
                      <option value = "!">!</option>
                    </select>
                  </div>
                  <div>
                    <label>Date and Time</label>
                    <input required type="datetime-local" value={data.target_value} placeholder='Target Value' onChange={(e)=>setData({...data, target_value:e.target.value})}></input>
                  </div>
                  </>)
              case "captain":
                return(
                  <div>
                    <label>Button Name</label>
                    <input required type="text" value={data.variable_name} placeholder='Button Name' onChange={(e)=>setData({...data, variable_name:e.target.value})}></input>
                  </div>
                )
              default:
                  return
          }
      })()}
      <div className='buttons'>
        <button className="delete-button" onClick={()=>onDelete(parent)}>Delete</button>
        <button className = "submit-button" type="submit">Submit</button>
      </div>
      </form>
      </div>

    </>, document.getElementById("portal")  // render it in the "portal" div in index.html
  )
}

// modal for editting command objects
function CommandModal({event, parent, getData, onSubmit, onCancel, onDelete}){

  const [data, setData] = useState(getData(parent))
  const [types, setTypes] = useState({"Hardware":"hardware", "Software":"software"})
  const [devices, setDevices] = useState({"-":null})
  const [funcs, setFuncs] = useState({"-":null})
  // const [html, setHtml] = useState("")

  let {eventid} = useParams()

  // set data defaults in case they are not defined yet
  useEffect(()=>{
    if(!data.type){
      setData({...data, type: Object.entries(types)[0][1]})
    }
  })


  // get all event devices of that type
  const getDevices = async () => {
    try{
      const request = await fetch(`${backend}/events/` + eventid + "/devices/" + data.type)
      if(!request.ok){
        return
      }
      const devs = await request.json()
      setDevices(devs)
    }
    catch{
      console.log("Could not connect to get devices")
    }
  }

  // get all devices based on type
  useEffect(()=>{
    getDevices()
  },[data.type])

  // useEffect(()=>{
    // if(!data.device){
    //   setData({...data, device: Object.entries(devices)[0][1]})
    //   return
    // }
    // TODO MAKE THIS WORK SOMEHOW
    // if(!Object.values(devices).includes(data.device)){
    //   setData({...data, device: Object.entries(devices)[0][1]})
    //   return
    // }
  // }, [devices])


  // get all functions available for a specific type
  const getFuncs = async () => {
    try{
      const request = await fetch(`${backend}/actions/functions/` + data.device)
      if(!request.ok){
        return
      }
      const functions = await request.json()
      setFuncs(functions)
    }
    catch{
      console.log("Could not connect to get functions")
    }
  }

  // reset selected function when device changes
  useEffect(()=>{
    getFuncs()
  },[data.device])

  // change function and erase arguments if necessary
  const changeFunction = (new_value) =>{
    if(new_value === data.function){
      return;
    }
    setData({...data, function: new_value, args: []});
  }

  // TODO make this work somehow
  // useEffect(()=>{
  //   if(!data.function){
  //     setData({...data, function: Object.entries(funcs)[0][1]})
  //     return
  //   }
  //   if(!Object.values(funcs).includes(data.function)){
  //     changeFunction(Object.entries(funcs)[0][1])
  //     return
  //   }
  // },[funcs])

  // ! lost cause
  // const getHtml = async () => {
  //   data.function = "select"
  //   try{
  //     const request = await fetch("http://127.0.0.1:8000/actions/html?function=" + data.function)
  //     if(!request.ok){
  //       console.log("Something went wrong " + request.status)
  //       return
  //     }
  //     let html = await request.json()
  //     setHtml(html)
  //   }
  //   catch{
  //     console.log("Could not connect")
  //   }
  // }

  // const loadArgs = () =>{
  //   const div = document.getElementById("args")
  //   const selects = div.querySelectorAll("select")
  //   const inputs = div.querySelectorAll("input")

  //   selects.forEach(select => {
  //     select.value = data[select.id]
  //   });
  //   inputs.forEach(input => {
  //     input.value = data[input.id]
  //   });
  // }

  // const getArgs = () => {
  //   // get args div referrence
  //   const div = document.getElementById("args")

  //   // get referrence to all select and input tags in div
  //   const selects = div.querySelectorAll("select")
  //   const inputs = div.querySelectorAll("input")

  //   // assign all those values to a key in args
  //   selects.forEach(select => {
  //     // args[select.id] = select.value
  //     const key = select.id
  //     const value = select.value
  //     data[key] = value
  //     setData(data)
  //   });

  //   inputs.forEach(input => {
  //     // args[input.id] = input.value
  //     const key = input.id
  //     const value = input.value
  //     data[key] = value
  //   })
  // }
  const handleSubmit = (e) =>{
    e.preventDefault()
    onSubmit(data, parent)
  }

  // get global variables
  const [variables, setVariables] = useState({})

  useEffect(()=>{
    const getVariables = async()=>{
      const response = await fetch(`${backend}/events/${eventid}/actions/variables/global/`)

      if(!response.ok){
        console.log("Error retrieving global variables " + response.status)
      }

      const vd = await response.json()
      console.log(vd)
      setVariables(vd)
    }

    getVariables()
  }, [])


  return ReactDom.createPortal(
  <>
  <div className='overlay' onClick={() => onCancel()}></div>
  <div className='modal'>
    <div className='header-div'>
      <text onClick={() => onCancel()}>&times;</text>
      <h2>Edit Command</h2>
    </div>
    {/* <form onSubmit={handleSubmit}> */}
    <form onSubmit={handleSubmit}>
    <div>
      <label>Name</label>
      <input type='text' required placeholder='Name' value={data.name} onChange={(e)=>{setData({...data, name: e.target.value})}}></input>
    </div>
    <div>
      <label>Type</label>
      <select value={data.type} onChange={(e)=>{setData({...data, type: e.target.value})}}>
      {Object.entries(types).map(([name, value]) => (
        <option value={value}>
          {name}
        </option>
      ))}
      </select>
    </div>
    <div>
      <label>Device</label>
      <select name ="device" required value={(data.device) ? data.device : ""} onChange={(e)=>{setData({...data,device: e.target.value})}}>
        <option value="">-</option>
        {Object.entries(devices).map(([name, value]) => (
          <option value={value}>
            {name}
          </option>
        ))}
      </select>
    </div>
    <div>
      <label>Function</label>
      <select required value={(data.function) ? data.function : ""} onChange={(e)=>changeFunction(e.target.value)}>
        <option value="">-</option>
        {Object.entries(funcs).map(([name, value]) => (
          <option value={value}>
            {name}
          </option>
        ))}
      </select>
    </div>
    {/* <div className="args" id="args" dangerouslySetInnerHTML={{__html: html}}/> */}
    <div>
      {(()=>{
          switch(data.function){
              case "toggle_light":
                if(!data.args[0]){
                  const new_args = [...data.args]
                  new_args[0] = "toggle"
                  setData({...data, args: [...new_args]})
                }
                return(
                <>
                <label>Toggle type</label>
                <select required value={data.args[0]} onChange={(e)=>{const new_args = [...data.args]; new_args[0]=e.target.value;setData({...data,args:[...new_args]})}}>
                  <option value="toggle">Toggle</option>
                  <option value="on">ON</option>
                  <option value="off">OFF</option>
                </select>
                </>)
              case "change_color":
                return(
                  <>
                  <div>
                    <label>Mode</label>
                    <select required value={data.args[0]} onChange={(e)=>{const new_args = [...data.args]; new_args[0]=e.target.value;setData({...data,args:[...new_args]})}}>
                      <option value="">-</option>
                      <option value="set">Set</option>
                      <option value="fade">Fade</option>
                    </select>
                    <label>Color</label>
                    <select required value={data.args[1]} onChange={(e)=>{const new_args = [...data.args]; new_args[1]=e.target.value;setData({...data,args:[...new_args]})}}>
                      <option value="">-</option>
                      <option value="on">ON</option>
                      <option value="red">Red</option>
                      <option value="blue">Blue</option>
                      <option value="green">Green</option>
                      <option value="yellow">Yellow</option>
                      <option value="cyan">Cyan</option>
                      <option value="pink">Pink</option>
                      <option value="off">OFF</option>
                    </select>
                  </div>
                  </>)
              case "edit_variable":
                // const new_args = [...data.args]
                data.args[0] = null  // user id
                if(!data.args[1]){
                  data.args[1] = ""  // variable name
                }
                if(!data.args[2]){
                  data.args[2] = "set" // mode
                }

              return(
              <>
              <div>
              <label>Variable name</label>
              <select required value={data.args[1]} onChange={(e)=>{const new_args = [...data.args]; new_args[1]=e.target.value;setData({...data,args:[...new_args]})}}>
              <option value={""}>-</option>
              {Object.entries(variables).map(([name, value]) => (
                <option value={value}>
                  {name}
                </option>
                ))}
              </select>
              </div>
              <div>
                <label>Mode</label>
                <select required value = {data.args[2]} onChange={(e)=>{const new_args = [...data.args]; new_args[2]=e.target.value;setData({...data,args:[...new_args]})}}>
                  <option value={"set"}>Set</option>
                  <option value={"add"}>Add</option>
                </select>
              </div>
              <div>
                <label>Value</label>
                <input required type='number' placeholder='Value' value={data.args[3]} onChange={(e)=>{const new_args = [...data.args]; new_args[3]=e.target.value;setData({...data,args:[...new_args]})}}></input>
              </div>
              </>) 
              default:
                  return
          }
      })()}
    </div>
    <div className='buttons'>
        <button className="delete-button" onClick={()=>onDelete(parent)}>Delete</button>
        {/* <button onClick={()=>onSubmit(data, parent)}>Submit</button> */}
        <button className="submit-button" type="submit">Submit</button>
    </div>
    </form>
  </div>

  </>, document.getElementById("portal")  // render it in the "portal" div in index.html
  )
}

const DeviceModal = ({id: id, name,type, address, port, onCancel, onSubmit, onDelete}) => {

  const [data, setData] = useState({id:id, name: name, type:type, address: address, port: port})
  return ReactDom.createPortal(
    <>
    <div className='overlay' onClick={onCancel}></div>
    <div className='modal'>
      <form onSubmit={(e)=>onSubmit(e, data)}>
      <div className='header-div'>
        <text onClick={() => onCancel()}>&times;</text>
        <h2>Edit Device</h2>
      </div>
        <div>
          <label>Device name</label>
          <input required value={data.name} type="text" placeholder='Device Name' onChange={(e)=>setData({...data, name: e.target.value})}></input>
        </div>
        <div>
          <label>Device Type</label>
          <input required value={data.type} type="text" placeholder='Device Type' onChange={(e)=>setData({...data, type: e.target.value})}></input>
        </div>
        <div>
          <label>Device address</label>
          <input required value={data.address} type="text" placeholder='Device Address' onChange={(e)=>setData({...data, address: e.target.value})}></input>
        </div>
        <div>
          <label>Device port</label>
          <input required value={data.port} type="number" placeholder='Device Port' onChange={(e)=>setData({...data, port: e.target.value})}></input>
        </div>
        <div className='buttons'>
          <button className="delete-button" onClick={()=>onDelete()}>Delete</button>
          <button className="submit-button" type='submit'>Submit</button>
        </div>
      </form>
    </div>
    </>, document.getElementById("portal")
  )
}


export default Modal