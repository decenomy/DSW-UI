import React, { useEffect, useState } from 'react';
import { get, post } from 'utils/requests';
import { ToastContainer, toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';


export function LoginForm() {
    const navigate = useNavigate();
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
        (response) => { if  (response.hasOwnProperty("error") )  { toast.error(response["error"]); }  else { toast.success(response["success"]); localStorage.setItem('variableName', 'bla'); setTimeout(() => { navigate('/dash')  }, 2000); } },
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
      <ToastContainer />
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
