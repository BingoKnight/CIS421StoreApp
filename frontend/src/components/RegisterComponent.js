import React, { useState } from 'react';
import { Redirect } from 'react-router-dom';
import $ from 'jquery';
import axios from 'axios';

const registerUser = setIsSubmitted => {

    const newUserObj = {
        'name': $('#register-name-input').val(),
        'email': $('#register-email-input').val(),
        'password': $('#register-password-input').val()
    };

    console.log('registration user obj: ', newUserObj);

    axios.post('http://localhost:8000/api/user/addUser/', newUserObj)
        .then(res => {
            if(res.status === 200)
                setIsSubmitted(true);
        })
};

const RegisterComponent = () => {

    const [isSubmitted, setIsSubmitted] = useState(false);

    if(isSubmitted)
        return <Redirect to={'/'} />

    return (
        <div className="container mt-5">

            <h2 className={'title'}>Registration</h2>
            <div className="form-group mt-5">
                <div className="row">
                    <div className="col-sm-1"><span>Name</span></div>
                    <div className="col"><input type="text" id='register-name-input' className={'form-control'}/></div>
                </div>
                <div className="row mt-2">
                    <div className="col-sm-1"><span>Email</span></div>
                    <div className="col"><input type="text" id={'register-email-input'} className={'form-control'}/></div>
                </div>
                <div className="row mt-2">
                    <div className="col-sm-1"><span>Password</span></div>
                    <div className="col"><input type="password" id='register-password-input' className={'form-control'}/></div>
                </div>
                <div className="row mt-2">
                    <div className="col">
                        <button className={'btn btn-primary w-100'} onClick={() => registerUser(setIsSubmitted)}>Register</button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default RegisterComponent