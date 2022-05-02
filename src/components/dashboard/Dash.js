import React, { useEffect, useState } from 'react';
import { get } from 'utils/requests';
import Navbar from 'components/navbar/Navbar';
import Titlebar from 'components/titlebar/Titlebar';

export function Dash() {

const [getInfo, setGetInfo] = useState([]);
useEffect(() => {
    
    get(
        'api/getinfo',
        (response) => alert(JSON.stringify(response)),
        //(response) => setGetInfo(response),
        (error) => console.error(error)
    )
    }, []);

return (
    <div className='container'>
    <Titlebar />
    <Navbar />
    <div className="columns">
      <div className="column">
      <div className="box">
        <p id="blocks">Latest block: {getInfo["blocks"]} </p>
        <p>Wallet version: </p>
        <p id="conn">Connections: </p>
        <p id="stake">Staking status: </p>
        <p id ="balance">Balance: </p>
      </div>
      </div>
      <div className="column">
      <div className="box">
        <p id="mymn">My masternodes: </p>
        <p id="mntotal">Total: </p>
      </div>
      </div>
      <div className="column">
      <div className="box">
        <p>1  =  EUR</p>
        <p>1  =  BTC</p>
      </div>
      </div>

    </div>
      <div className="columns">
      <div className="box">
      <table id="txs" className="display table is-fullwidth is-hoverable"  width="100%">
    <thead>
        <tr>
            <th>Type</th>
            <th>TXID</th>
            <th>Amount</th>
            <th>Time</th> 
        </tr>
    </thead></table>
    </div>
    </div>
    </div>
    );
}

export default Dash;
