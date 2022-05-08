import React, { useEffect, useState } from 'react';
import { get } from 'utils/requests';
import Navbar from 'components/navbar/Navbar';
import {QRCodeCanvas} from 'qrcode.react';

export function ReceivePage() {

const [getNewAddr, setGetNewAddr] = useState([]);
  useEffect(() => {

    get(
      'api/newaddr',
      (response) => setGetNewAddr(response),
      (error) => console.error(error)
    )
  }, []);


return (
<div className='container'>
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
    <input className="input" type="text" value={getNewAddr["address"]} id="address" readonly />
    </div>
</div>
<input className="button is-info is-rounded is-outlined" type="submit" value="Copy" id="copy-button" />
</div>
</div>

<div className="column is-one-fifth">

</div>
</div>
</div>
);
}
        
export default ReceivePage;