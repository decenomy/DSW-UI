import 'index.scss';

import * as serviceWorker from 'serviceWorker';

import App from 'components/App';
import { Provider } from 'react-redux';
import React from 'react';
import ReactDOM from 'react-dom';
import store from 'state/store';
import { HashRouter } from 'react-router-dom'
import 'bulma/css/bulma.min.css';
import 'react-toastify/dist/ReactToastify.css';


ReactDOM.render(
  <React.StrictMode>
    <Provider store={ store }>
    <HashRouter>
      <App />
    </HashRouter>
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
