import React, { useState } from "react";
import {Link} from 'react-router-dom'
import $ from 'jquery';
import Cookies from 'js-cookie';
import axios from 'axios';
import {connect, useDispatch} from "react-redux";
import {setIsLoggedIn} from "../../actions/users";


const loginUser = dispatch => {
    const loginObj = {
        'email': $('#login-email').val(),
        'password': $('#login-password').val()
    }

    axios.post('http://localhost:8000/api/user/login/', loginObj)
        .then(res => {
            if(res.status === 200) {
                Cookies.set('user_id', res.data['id']);
                Cookies.set('user_name', res.data['name']);
                dispatch(setIsLoggedIn(true));
            }
        })
}

const LoginForm = props => {
    if(Cookies.get('user_id')){
        return (
            <div className="collapse navbar-collapse" id="navbarSupportedContent">
                <span className="navbar-nav mr-auto"/>
                <form className="form-inline my-2 my-lg-0">
                    <span className={'mr-3'}>Hello {Cookies.get('user_name')}!</span>
                    <button className="btn btn-primary my-2 mr-sm-2 my-sm-0" type="submit"
                            onClick={() => {Cookies.remove('user_id', {path: ''}); Cookies.remove('user_name', {path: ''})}}>
                        Sign Out
                    </button>
                </form>
            </div>
        )
    } else {
        return (
            <div className="collapse navbar-collapse" id="navbarSupportedContent">
                <span className="navbar-nav mr-auto"/>
                <form className="form-inline my-2 my-lg-0">
                    <input className="form-control mr-sm-2" placeholder="Email" id={'login-email'}/>
                    <input className="form-control mr-sm-2" type={'password'} placeholder="Password"
                           id={'login-password'}/>
                    <button className="btn btn-primary my-2 mr-sm-2 my-sm-0" type="submit"
                            onClick={() => loginUser(props.dispatch)}>Login
                    </button>
                    <Link class="btn btn-outline-success my-2 my-sm-0" type="submit"
                          to={'/register'}>Register</Link>
                </form>
            </div>
        )
    }
}

const Header = props => {
    let userName = '';

    const dispatch = useDispatch();

    const isLoggedIn = props.users.isLoggedIn;

    if(Cookies.get('user_id')){
        axios.get('http://localhost:8000/api/user/login/' + Cookies.get('user_id') + '/')
            .then(res => {
                userName = res.data['user']
            }, err => {
                Cookies.remove('user_id', {path: ''})
            })
    }

    return (
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container">
                <Link to='/' class="navbar-brand">Dashboard</Link>
                <Link to='/users' class="navbar-brand">Users</Link>
                <button class="navbar-toggler" type="button" data-toggle="collapse"
                        data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                        aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <LoginForm isLoggedIn={isLoggedIn} userName={userName} dispatch={dispatch} />
            </div>
        </nav>
    );
};

const mapStateToProps = state => {
    return {
        users : state.users
    }
}

export default connect(mapStateToProps)(Header)