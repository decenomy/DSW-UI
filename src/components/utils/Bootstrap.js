import React, { useState, useEffect } from 'react';
import Navbar from 'components/navbar/Navbar';


export function Bootstrap() {

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