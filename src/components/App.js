import React, { Fragment, useEffect, useState } from 'react';
import { get } from 'utils/requests';

import { Counter } from 'components/counter/Counter';
import Titlebar from 'components/titlebar/Titlebar';

import logo from 'logo.svg';
import styles from 'components/App.module.scss';

import 'bulma/css/bulma.min.css';


function App() {
  const [availableCoins, setAvailableCoins] = useState([]);
  useEffect(() => {

    get(
      'api/getcoins', // Route
      (response) => setAvailableCoins(response), // Response callback
      (error) => console.error(error) // Error callback
    )
  }, []);


  return (
    <Fragment>
      <Titlebar />

      <div className={ styles.app }>
        <header className={ styles['app-header'] }>
          <img src={ logo } className={ styles['app-logo'] } alt="logo" />
          <section class="section">
          <div class="container">
            <h1 class="title">
              Decenomy Standard Wallet UI
            </h1>
          </div>
          <div class="container">
            <div class="box">
            <form id="loginform">
            <div class="field">
            <label class="label">Wallet</label>
            <div class="control">
            <div class="select">
              <select id="coinselect" name="coinselect">
              {Object.keys(availableCoins).map(key => (
                <option value="{key}">{key}</option>
              ))}
              </select>
            </div>
            </div>
          </div>
            <div class="field">
              <label class="label">Dashdboard Password</label>
              <div class="control">
                <input class="input" type="password" placeholder="" name="password" id="password" />
              </div>
            </div>
            <input class="button is-info is-rounded is-outlined" type="submit" value="Connect" />
          </form>
          </div>
          </div>
        </section>
        </header>
      </div>
    </Fragment>
  );
}

export default App;
