import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import "./programmer.css";
import Trigger from './triggers';
import Modal from "./modal"

// get backend ip and port from .env file
const backend = `http://${process.env.REACT_APP_BACKEND_IP}:${process.env.REACT_APP_BACKEND_PORT}`

const Programmer = () => {
  const [actions, setActions] = useState({"None":"none"})
  const [action, setAction] = useState("none")
  const [triggers, setTriggers] = useState([[], [], [], [], []]);
  const [modalType, setModalType] = useState(null)
  const [modalProps, setModalProps] = useState({})

  let {eventid} = useParams()

  // get list of available actions for the event
  const getActions = async () => {
    try{
      const request = await fetch(`${backend}/events/${eventid}/actions/`)
      if(!request.ok){
        console.log("Could not fetch actions, error: " + request.status)
        return
      }
      const data = await request.json()
      setActions(data)
    }
    catch{
      console.log("Could not connect to fetch actions")
    }
  }

  useEffect(()=>{
    getActions()
    setAction(Object.entries(actions)[0][1])
  },[eventid])

  // react component that opens the modal for creating triggers
  const Adder = ({column}) =>{
    
    // onclick function for adding triggers
    const addElement = (column) => {
      
      // check if the max amount of triggers has been reached
      if (triggers[column].length > 5){
        console.log("You reached the maximum")
        return;
      }
      
      // new trigger index
      const i = triggers[column].length
      
      // add empty trigger to state
      const newTriggers = [...triggers]
      const trigger = {}
      newTriggers[column].push(trigger);
      setTriggers(newTriggers);



      // open modal to input data
      // type depends on the column
      switch(column){
        case (triggers.length-1):
          // createCommand(column, i)
          createCommand(column, i)
          break;
        default:
          createTrigger(column, i)
      }
    }
  
    return(
      <div className='Adder' onClick={() => addElement(column)}>{(column === triggers.length-1) ? "Add a Command" : "Add a Trigger"}</div>
    )
  }

  // component for displaying command object
  const Command = ({display, index, onClick}) => {

    // for new commands, display predefined text
    if(display === undefined){
      display = "new command"
    }
  
    return (
      <div className='Trigger'>
      <div className={(index>0) ? "line-or-before" : "line-and"}></div>
      <div className = "display" onClick={onClick}>
        {display}
      </div>
      <div className={"line-and"}></div>
      </div>
    )
  }

  // edit action name
  const editAction = () => {
    setModalProps({name:action, onCancel:closeModal, onDelete: deleteAction,onSubmit:submitActionEdit})
    setModalType("action")
  }

  // create blank action from modal
  const createAction = () => {
    const handleCancel = () =>{
      setAction(Object.entries(actions)[0][1])
      closeModal()
    }
    const handleSubmit = async (action_name) =>{
      // setTriggers([[],[],[],[],[]])
      // setAction(action_name)
      // alert(action_name)
      // onSave()
      const request = await fetch(`${backend}/events/${eventid}/actions/`,{
        method: "POST",
        headers:{"content-type":"application/json"},
        body:JSON.stringify({"triggers":[[],[],[],[],[]], "action_name":action_name})
      })
      

    }
    setModalProps({name:"", onCancel:handleCancel, onDelete: handleCancel, onSubmit:handleSubmit})
    setModalType("action")
  }

  // submit action name change
  const submitActionEdit = async (new_name) => {
    try{
      const request = await fetch(`${backend}/events/${eventid}/actions/${action}/`, {
        method:"PUT",
        headers:{
          "Content-type":"application/json"
        },
        body:JSON.stringify({"new_name":new_name})
      })

      if(!request.ok){
        console.log("Could not change Action name, error " + request.status)
        return
      }

      closeModal()
      getActions()
    }
    catch{
      console.log("Error when trying to edit Action name")
    }
  }

  // delete action button event
  const deleteAction = async () =>{
    try{
      const request = await fetch(`${backend}/events/${eventid}/actions/${action}/`,{
        method: "DELETE",
      })
      if(!request.ok){
        console.log("Could not delete action " + request.status)
        return
      }
    }
    catch{
      console.log("Could not connect to server to delete action")
    }
  }

  // open modal to create new trigger
  const createTrigger = (column, key) => {
    setModalProps({event: eventid, parent:[column,key],getData:getElementData, onSubmit:saveElementData, onCancel:(()=>{deleteElement([column, key])}), onDelete:deleteElement})
    setModalType("trigger")
  }

  // open command modal to create
  const createCommand = (column, key) =>{
    setModalProps({event: eventid, parent:[column,key],getData:getElementData, onSubmit:saveElementData, onCancel:(()=>{deleteElement([column, key])}), onDelete:deleteElement})
    setModalType("command")
  }


  // open modal to edit trigger data upon click
  const editTrigger = (column, key) => {
    setModalProps({event: eventid, parent:[column,key],getData:getElementData, onSubmit:saveElementData,onCancel:closeModal, onDelete:deleteElement})
    setModalType("trigger")
  }

  // open command modal to edit
  const editCommand = (column, key) => {
    setModalProps({event: eventid, parent:[column,key],getData:getElementData, onSubmit:saveElementData,onCancel:closeModal, onDelete:deleteElement})
    setModalType("command")
  }

  // delete element from state, called by modal
  const deleteElement = (element) => {
    
    const [column, index] = element;
    
    let data = [...triggers]
    data[column].splice(index,1)

    setTriggers([...data])
    closeModal();
  }

  // called by modal to retrieve element data from state
  const getElementData = (element) => {
    const [column, index] = element
    return triggers[column][index];
  }


  // save new element data to state
  const saveElementData = (newElementData, element) => {
    let elementData = [...triggers];
    const [column, index] = element
    elementData[column][index] = newElementData;
    setTriggers(elementData);
    closeModal();
  }


  // function to close modal
  const closeModal = () => {
    setModalType(null);
    setModalProps({})
  }


  // generate react components based on state, per column
  const render = (column) => {
    const innerdivs = []
    const count = triggers[column].length

    if (count === 0){
      innerdivs.push(<Adder  column = {column}/>)
      return innerdivs
    }

    if(column === triggers.length-1){
      for (let i = 0; i < count; i++){
        innerdivs.push(<Command index= {i} display = {triggers[column][i].name} onClick={() => editCommand(column, i)}/>)
      }
    }
    else{
      for (let i = 0; i < count; i++){
        // value trigger display
        let todisplay = `${triggers[column][i].variable_name} ${triggers[column][i].condition} ${triggers[column][i].target_value}`
        // time trigger display
        if(triggers[column][i].type === "time"){
          todisplay = `TIME PASSED ${triggers[column][i].target_value}s`
        }
        // captain trigger display
        if(triggers[column][i].type === "captain"){
          todisplay = `CAPTAIN TRIGGER ${triggers[column][i].variable_name}`
        }
        // date trigger display
        if(triggers[column][i].type === "date"){
          
          const date = new Date(triggers[column][i].target_value)
          const day = `${date.getDate()}`
          const month = (date.getMonth() < 8) ? `0${date.getMonth()+1}` : `${date.getMonth()+1}`
          const year = `${date.getFullYear()}`
          const hour = (date.getHours() < 8) ? `0${date.getHours()}` : `${date.getHours()}`
          const minutes = (date.getMinutes() < 8) ? `0${date.getMinutes()}` : `${date.getMinutes()}`
          todisplay = `DATE ${triggers[column][i].condition} ${day}-${month}-${year} ${hour}:${minutes}`
        }
        innerdivs.push(<Trigger index= {i} display = {todisplay} onClick={() => editTrigger(column, i)}/>)
      }
    }

    if (count === 5){
      return innerdivs;
    }
    
    innerdivs.push(<Adder  column = {column}/>)

    for (let i = count-1; i < 4; i++){
      innerdivs.push(<p></p>)
    }

    return innerdivs
  }

  // send trigger data to the backend via POST
  const onSave = async () => {
    console.log(triggers)
    try{
      const request = await fetch(`${backend}/events/${eventid}/actions/`, {
        method: "POST",
        headers:{
          "content-type": "application/json"
        },
        body: JSON.stringify({"triggers": triggers, "action_name":action})
      })
      if(!request.ok){
        console.log("Could not submit action, error:  " + request.status)
        return
      }
      const data = await request.json()
      console.log(data)
    }
    catch{
      console.log("Could not connect to submit action")
    }
  }

  // get trigger data from the backend via GET
  const loadAction = async () => {
    try{
      const request = await fetch(`${backend}/events/${eventid}/actions/${action}`)
      if(!request.ok){
        console.log("Something went wrong " + request.status)
        return
      }
      const data = await request.json()
      console.log(data)
      setTriggers(data)
    }
    catch{
      console.log("Could not connect to download action")
    }
  }
  
  // every time the user selects another action from the dropdown,
  // download the action data
  useEffect(()=>{
    setAction(Object.entries(actions)[0][1])
    loadAction()
  },[actions])


  useEffect(()=>{
    if(action === ""){
      // alert("you tried to add a new action")
      createAction()
    }
    else{
      loadAction()
    }
  },[action])


  return(
    <div>
      {/* <div>{Object.entries(test)[0][0]}</div> */}
      <Modal type = {modalType} props = {modalProps}/>
      <div className='programmer-select'>
        <select value={action} onChange={(e)=>{setAction(e.target.value)}}>
        {Object.entries(actions).map(([name, value]) => (
          <option value={value}>
            {name}
          </option>
        ))}
        <option value={""}>Create a new Action</option>
        {/* <option value={"test bitches"}>test bitches</option> */}
        </select>
        <button onClick={()=> editAction()}>Edit</button>
      </div>
      
      <div className= "Programmer">
        {triggers.map((_, column) => (
          <div className="programmer-columns" key = {column}>
            {render(column)}
          </div>
        ))}
      </div>

      <button className="export-btn" onClick={() => onSave()}>Save</button>
      <button className="clear-btn" onClick={() => setTriggers([[],[],[],[],[]])}>Clear</button>
    </div>
  )
};

export default Programmer;
