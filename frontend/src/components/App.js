import React, {Component, Fragment} from 'react';
import ReactDOM from 'react-dom';

import Header from './layout/Header'
import ProductDashboard from './products/ProductDashboard';

import { Provider } from 'react-redux';
import store from '../store';

class App extends Component{
    render() {
        return (
            <Provider store={store}>
                <Fragment>
                    <Header/>
                    <div className="container">
                        <ProductDashboard/>
                    </div>
                </Fragment>
            </Provider>
        );
    }
}

ReactDOM.render(<App />, document.getElementById("app"));
