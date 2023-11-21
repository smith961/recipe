import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/main.css'
import React, {useState, useEffect} from 'react';
import { ReactDOM } from 'react';
import Navbar from './components/Navbar';

import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import HomePage from './components/Home';
import SignUpPage from './components/SignUp';
import LoginPage from './components/Login';
import CreateRecipe from './components/CreateRecipe';

function App() {

  

  
  return (
   <Router>
    <div className="">
      <Navbar/>
      <Switch>
      <Route path='/create_recipe'>
          <CreateRecipe/>
        </Route>
      <Route path='/login'>
          <LoginPage/>
        </Route>
      <Route path='/signup'>
          <SignUpPage/>
        </Route>
        <Route path='/'>
          <HomePage/>
        </Route>

      </Switch>
    </div>
    </Router>
   
  );
}

export default App;
