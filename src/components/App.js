import React, { } from 'react';
import { MemoryRouter, Route, Routes } from "react-router-dom";

import LoginForm from 'components/forms/LoginForm';
import Dash from './dashboard/Dash';

import logo from 'logo.svg';
import styles from 'components/App.module.scss';

const IndexPage = () => {
  return (<>
    <div className={ styles.app }>
    <div className='navigation'>
    </div>
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
  </>)
};

const Dashboard = () => {
  return <Dash />;
};

function App() {
  return (
  <MemoryRouter>
    <Routes>
      <Route path="/" element={<IndexPage />} />
      <Route path="/dash" element={<Dashboard />} />
    </Routes>
  </MemoryRouter>
  );
}


export default App;
