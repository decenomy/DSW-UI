import React, { useEffect, useState, useRef } from 'react';
import { get } from 'utils/requests';
import Navbar from 'components/navbar/Navbar';
import Titlebar from 'components/titlebar/Titlebar';

export function Dash() {

const [getInfo, setGetInfo] = useState([]);
const [getPrice, setGetPrice] = useState([]);
useEffect(() => {
    
    get(
        'api/getinfo',
        (response) => setGetInfo(response),
        (error) => console.error(error)
    )
    }, []);

useEffect(() => {

  get(
      'api/price',
      (response) => setGetPrice(response),
      (error) => console.error(error)
  )
  }, []);



const [isPaused, setPause] = useState(false);
const ws = useRef(null);

useEffect(() => {
    ws.current = new WebSocket("ws://localhost:8765");
    ws.current.onopen = () => console.log("ws opened");
    ws.current.onclose = () => console.log("ws closed");

    const wsCurrent = ws.current;

    return () => {
        wsCurrent.close();
    };
}, []);


useEffect(() => {
    if (!ws.current) return;

    ws.current.onmessage = e => {
        if (isPaused) return;
        const mydata = JSON.parse(e.data);
        
        if ('type' in mydata) {
          if (mydata["type"] == "block") {
            const updatedGetInfo = [...getInfo];
            updatedGetInfo["blocks"] = mydata["data"]["height"];
            setGetInfo(updatedGetInfo);
            }
            else if (mydata["type"] == "transaction") {
              alert("new tx");
            }
            /*
            else if (mydata["type"] == "getinfo") {
            const updatedGetInfo = [...getInfo];
            updatedGetInfo["staking status"] = mydata["data"]["staking status"];
            updatedGetInfo["balance"] = mydata["data"]["balance"];
            updatedGetInfo["connections"] = mydata["data"]["connections"];
            setGetInfo(updatedGetInfo);
            }
            */
            else if (mydata["type"] == "masternodes") {
              alert("mn");
            }
        }
    };
}, [isPaused]);

return (
    <div className='container'>
    <Titlebar />
    <Navbar />
    <div className="columns">
      <div className="column">
      <div className="box">
        <p>Latest block: {getInfo["blocks"]}</p>
        <p>Wallet version: {getInfo["version"]}</p>
        <p>Connections: {getInfo["connections"]}</p>
        <p>Staking status: {getInfo["staking status"]}</p>
        <p>Balance: {getInfo["balance"]}</p>
      </div>
      </div>
      <div className="column">
      <div className="box">
        <p>My masternodes: </p>
        <p>Total: </p>
      </div>
      </div>
      <div className="column">
      <div className="box">
        <p>1 {getPrice["coin"]} = {getPrice["eur"]} EUR</p>
        <p>1 {getPrice["coin"]} = {getPrice["btc"]} BTC</p>
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
