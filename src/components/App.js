import React, { Fragment, useEffect, useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';

import LoginForm from 'components/forms/LoginForm';
import Titlebar from 'components/titlebar/Titlebar';
import { Navbar } from './navbar/Navbar';

import logo from 'logo.svg';
import styles from 'components/App.module.scss';


function App() {

  return (

    <Fragment>
      <Titlebar />
      <div className={ styles.app }>
        <header className={ styles['app-header'] }>
          <img src={ logo } className={ styles['app-logo'] } alt="logo" />
          <section className="section">
          <div className="container">
            <h1 className="title">
              Decenomy Standard Wallet UI
            </h1>
          </div>
          <div className="container">
            <div className="box">
            <LoginForm />
          </div>
          </div>
        </section>
        </header>
      </div>
    </Fragment>
  );
}

export default App;
