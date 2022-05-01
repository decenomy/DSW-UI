import React, { Fragment, useEffect, useState } from 'react';
import { get, post } from 'utils/requests';

export function LoginForm() {

    const [text, setText] = useState('');
    const [coin, setCoin] = useState();
    
  
    const onInputChange = (event) => {
     setText(event.target.value);
    }

    const onSelectChange = (event) => {
      setCoin(event.target.value);
     }

    const onSubmit = (e) => {
      e.preventDefault();
      const req = { password: text, coin: coin }
      post(
        JSON.stringify(req),
        'login',
        (response) => alert(JSON.stringify(response)),
        (error) => console.error(error)
      )
    }

  const [availableCoins, setAvailableCoins] = useState([]);
  useEffect(() => {

  get(
      'api/getcoins',
      (response) => setAvailableCoins(response),
      (error) => console.error(error)
    )
  }, []);


  return (
    <form id="loginform" onSubmit={onSubmit} >
      <div className="field">
      <label className="label">Wallet</label>
      <div className="control">
      <div className="select">
        <select id="coinselect" name="coinselect" onChange={onSelectChange}>
         <option>Select a coin..</option>
        {Object.keys(availableCoins).map(key => (
          <option value={key}>{key}</option>
        ))}
        </select>
      </div>
      </div>
    </div>
      <div className="field">
        <label className="label">Dashdboard Password</label>
        <div className="control">
          <input className="input" type="password" placeholder="" name="password" id="password" onChange={onInputChange} />
        </div>
      </div>
      <input className="button is-info is-rounded is-outlined" type="submit" value="Connect"  />
    </form>
);
}

export default LoginForm;
