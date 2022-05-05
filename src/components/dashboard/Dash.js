import React, { useEffect, useState, useRef } from 'react';
import { get } from 'utils/requests';
import Navbar from 'components/navbar/Navbar';

export function Dash() {

  const [getInfo, setGetInfo] = useState([]);
  const [getPrice, setGetPrice] = useState([]);
  const [getMasternodes, setGetMasternodes] = useState([]);
  const [getMyMasternodes, setGetMyMasternodes] = useState([]);
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

  useEffect(() => {

    get(
      'api/mntotal',
      (response) => setGetMasternodes(response),
      (error) => console.error(error)
    )
  }, []);

  useEffect(() => {

    get(
      'api/mymn',
      (response) => setGetMyMasternodes(response),
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
        if (mydata["type"] === "block") {
          const updatedGetInfo = {...getInfo};
          updatedGetInfo.blocks = mydata["data"]["height"];
          setGetInfo(updatedGetInfo);
        }
        else if (mydata["type"] === "transaction") {
          console.log("new tx");
        }
        else if (mydata["type"] == "getinfo") {
        const updatedGetInfo = {...getInfo};
        updatedGetInfo["staking status"] = mydata["data"]["staking status"];
        updatedGetInfo.balance = mydata["data"]["balance"];
        updatedGetInfo.connections = mydata["data"]["connections"];
        setGetInfo(updatedGetInfo);
        }
        else if (mydata["type"] === "masternodes") {
          const updatedGetMasternodes = {...getMasternodes};
          updatedGetMasternodes.total = mydata["data"]["total"];
          setGetMasternodes(updatedGetMasternodes);
        }
      }
    };
  }, [isPaused, getInfo, getMasternodes]);

  const { blocks,
    version,
    connections,
    ['staking status']: stakingStatus,
    balance
  } = getInfo;

  const {
    coin,
    eur,
    btc
  } = getPrice;

  const {
    total
  } = getMasternodes;

  return (
    <div className='container'>
      <Navbar />
      <div className="columns">
        <div className="column">
          <div className="box">
            <p>Latest block: {blocks}</p>
            <p>Wallet version: {version}</p>
            <p>Connections: {connections}</p>
            <p>Staking status: {stakingStatus}</p>
            <p>Balance: {balance}</p>
          </div>
        </div>
        <div className="column">
          <div className="box">
            <p>My masternodes: {getMyMasternodes.length} </p>
            <p>Total: {getMasternodes.total}</p>
          </div>
        </div>
        <div className="column">
          <div className="box">
            <p>1 {coin} = {eur} EUR</p>
            <p>1 {coin} = {btc} BTC</p>
          </div>
        </div>

      </div>
      <div className="columns">
        <div className="box">
          <table id="txs" className="display table is-fullwidth is-hoverable" width="100%">
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
