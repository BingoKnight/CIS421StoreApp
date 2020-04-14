import React, {Component, Fragment} from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter as Router, Route} from 'react-router-dom';

import Header from './layout/Header'
import ProductDashboard from './products/ProductDashboard';
import RegisterComponent from "./RegisterComponent";

import { Provider } from 'react-redux';
import store from '../store';

class App extends Component{
    render() {
        return (
            <Provider store={store}>
                <Fragment>
                    <Router>
                        <Header/>
                        <Route path={'/register'} component={RegisterComponent} />
                        <Route exact path={'/'} component={ProductDashboard} />
                    </Router>
                </Fragment>
            </Provider>
        );
    }
}

ReactDOM.render(<App />, document.getElementById("app"));
