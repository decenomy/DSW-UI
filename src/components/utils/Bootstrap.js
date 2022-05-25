import React, { useState, useEffect } from 'react';
import Navbar from 'components/navbar/Navbar';
import { NativeEventSource, EventSourcePolyfill } from 'event-source-polyfill';


export function Bootstrap() {
	const EventSource = NativeEventSource || EventSourcePolyfill;
	const [data, setData] = useState(null)
	useEffect(() => {
		let eventSource = new EventSourcePolyfill("http://localhost:3001/bootstraplog", { headers : { 'Authorization': 'Bearer ' + localStorage.getItem('Authorization')} })
		 eventSource.onmessage = (e) => {
			setData(alert(e.data))
			}
		/*
		eventSource.addEventListener('newEntry', e =>
		updateLogs(e.data)
	  )
	  eventSource.addEventListener('close', () =>
		eventSource.close()
	  )
  */
	  return (() => eventSource.close() )
	}, [])
    return (
        <div className='container'>
          <Navbar />
          <div className="container">
	<div className="columns is-centered is-mobile">	
		<div className="column is-muted notification is-four-fifths">
			<h1 className="title">Bootstrap installer</h1>
			<h2 className="subtitle">Please do not refresh this page.</h2>
			<div id="progress"></div>
		</div>
	</div>
</div>
<div className="container">
	<div className="columns is-centered is-mobile">	
		<div className="column is-dark notification is-four-fifths">
			<div className="is-size-7 has-text-warning" id="display">
				<ul id="display_list">
				</ul>
			</div>
		</div>
	</div>
</div>
        </div>
 );
}
export default Bootstrap;