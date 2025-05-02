import React from 'react'

const Trigger = ({display, index, onClick}) => {

  // for new triggers, instead of "that", display
  // proper text
  if(display === "undefined undefined undefined"){
    display = "new trigger"
  }

  return (
    <div className='Trigger'>
    <div className={(index>0) ? "line-or-before" : "line-and"}></div>
    <div className = "display" onClick={onClick}>
      {display}
    </div>
    <div className={(index>0) ? "line-or-after" : "line-and"}></div>
    </div>
  )
}

export default Trigger

