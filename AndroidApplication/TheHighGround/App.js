import React, { Component } from 'react';
import { View, StyleSheet, Button, ToastAndroid} from 'react-native';
// import firebase from 'react-native-firebase';
import t from 'tcomb-form-native'; // 0.6.9

const Form = t.form.Form;

const User = t.struct({
  FirstName: t.String,
  LastName: t.maybe(t.String),
  PhoneNumber: t.Number,
  terms: t.Boolean
});

// //////// FIREBASE SETUP /////////////
// var firebaseConfig = {
//   apiKey: "AIzaSyCvEmaBPGgcIsDgA5QwNuhhm9Au5tAPsdI",
//   authDomain: "intricate-yew-257819.firebaseapp.com",
//   databaseURL: "https://intricate-yew-257819.firebaseio.com",
//   projectId: "intricate-yew-257819",
//   storageBucket: "intricate-yew-257819.appspot.com",
//   messagingSenderId: "473804431377",
//   appId: "1:473804431377:web:74f33de43cf70559ed11b0",
//   measurementId: "G-GBG195G048"
// };
// // Initialize Firebase
// firebase.initializeApp(firebaseConfig);


const options = {
  fields: {
    FirstName: {
      error: 'Your first name is needed to be added to our database!'
    },
    PhoneNumber: {
      error: 'Your phone number is used to send alerts to your phone with emergency mapping information!'
    },
    terms: {
      label: 'Agree to Terms',
    },
  },
};

const formStyles = {
  ...Form.stylesheet,
  controlLabel: {
    normal: {
      color: 'blue',
      fontSize: 18,
      marginBottom: 7,
      fontWeight: '600'
    },
    error: {
      color: 'red',
      fontSize: 18,
      marginBottom: 7,
      fontWeight: '600'
    }
  }
}


///////////////////////////////////////////////////////////////////////////////////////

export default class App extends Component {

  handleSubmit = () => {
    const value = this._form.getValue(); // use that ref to get the form value
    console.log('value: ', value);
    if (value !== null){
      ToastAndroid.show("You've been registered ".concat(value.FirstName,"!"), 15);
    };

    //


  }
  render() {
    return (
      <View style = {styles.container} >
        <Form
          ref={c => this._form = c}
          type={User}
          options={options}
        />
        <Button
          title="Sign Up!"
          onPress={this.handleSubmit}
        />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    justifyContent: 'center',
    marginTop: 50,
    padding: 20,
    backgroundColor: '#ffffff',
  },
});
