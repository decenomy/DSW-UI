import React, { useEffect, useState, useRef } from 'react';
import { get } from 'utils/requests';
import Navbar from 'components/navbar/Navbar';
import {QRCodeCanvas} from 'qrcode.react';
import { ToastContainer, toast } from 'react-toastify';

export function ReceivePage() {

const [getNewAddr, setGetNewAddr] = useState([]);
  useEffect(() => {

    get(
      'api/newaddr',
      (response) => setGetNewAddr(response),
      (error) => console.error(error)
    )
  }, []);
  const textAreaRef = useRef(null);
  function copyToClipboard(e) {
    textAreaRef.current.select();
    document.execCommand('copy');
    // This is just personal preference.
    // I prefer to not show the the whole text area selected.
    e.target.focus();
    toast.success("Address copied!");
  };

return (
<div className='container'>
<ToastContainer />
<Navbar />
<div className="columns">
<div className="column is-one-fifth">
<QRCodeCanvas value={getNewAddr["address"]} />
</div>
<div className="column">
<div className="box">
<div className="field">
    <label className="label">Receive</label>
    <div className="control">
    <input className="input" ref={textAreaRef} type="text" value={getNewAddr["address"]} id="address" readonly />
    </div>
</div>
<input className="button is-info is-rounded is-outlined" onClick={copyToClipboard} type="submit" value="Copy" id="copy-button" />
</div>
</div>

<div className="column is-one-fifth">

</div>
</div>
</div>
);
}
        
export default ReceivePage;