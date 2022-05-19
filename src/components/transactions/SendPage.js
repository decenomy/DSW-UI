import React, { useEffect, useState, useRef } from 'react';
import Navbar from 'components/navbar/Navbar';
import { ToastContainer, toast } from 'react-toastify';

export function SendPage() {

return (
<div className="container">
  <ToastContainer />
    <div className="columns">
      <div className="column is-one-fifth">
      
      </div>
      <div className="column">
      <div className="box">
      <form method="POST" id="sendform">
      <div className="field">
        <label className="label">Address</label>
        <div className="control">
          <input className="input" type="text" placeholder="" name="address" id="address" />
        </div>
      </div>
      <div className="field">
        <label className="label">Amount</label>
        <div className="control">
          <input className="input" type="number" placeholder="123.45" name="amount" id="amount" min="0" step="0.00000001" />
        </div>
      </div>
      <div className="field">
        <label className="label">Wallet Passphrase</label>
        <div className="control">
          <input className="input" type="password" placeholder="" name="passphrase" id="passphrase" />
        </div>
      </div>
      <input className="button is-info is-rounded is-outlined" type="submit" value="Send" />
    </form>
      </div>
      </div>
     
      <div className="column is-one-fifth">
      
      </div>

    </div>
    </div>
);
}
        
export default SendPage;