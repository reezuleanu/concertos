import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import "./sidebar.css"

const Sidebar = ({option}) => {
  
  if(!option){
    option = "overview"
  }

  const [getOption, setOption] = useState("overview")

  let {eventid} = useParams()

  // change state whenever argument changes
  useEffect(() =>{
    setOption(option);
  }, [option])

  // change active link whenever state changes
  useEffect(() => {
    const links = document.querySelectorAll(".sidebar a");
    links.forEach(link => {
      if (link.innerText.toLowerCase() === getOption) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }, [getOption]);

  // get base url for absolute path redirection
  const baseurl = window.location.origin

  return (
    <div className="sidebar">
      <ul>
        {/* <li><a href={`${baseurl}/settings/${eventid}/overview`} className="active">Overview</a></li> */}
        {/* <li><a href={`${baseurl}/settings/${eventid}/general`}>General</a></li> */}
        <li><a href={`${baseurl}/settings/${eventid}/actions`}>Actions</a></li>
        <li><a href={`${baseurl}/settings/${eventid}/variables`}>Variables</a></li>
        <li><a href={`${baseurl}/settings/${eventid}/devices`}>Devices</a></li>
        {/* <li><a href={`${baseurl}/settings/${eventid}/user actions`}>User Actions</a></li> */}
        <li><a href={`${baseurl}/settings/${eventid}/captain`}>Captain's Cabin</a></li>
      </ul>
    </div>
  )
}

export default Sidebar