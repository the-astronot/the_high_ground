import React, { Component } from 'react';
import { View, StyleSheet, Button, ToastAndroid} from 'react-native';

import t from 'tcomb-form-native'; // 0.6.9

const Form = t.form.Form;

const User = t.struct({
  FirstName: t.String,
  LastName: t.maybe(t.String),
  PhoneNumber: t.Number,
  terms: t.Boolean
});

export default class App extends Component {

  handleSubmit = () => {
    const value = this._form.getValue(); // use that ref to get the form value
    console.log('value: ', value);
    ToastAndroid.show("You've been registered ".concat(value.FirstName,"!"), 15);
  }

  render() {

    return (
      <View style = {styles.container} >
        <Form
          ref={c => this._form = c}
          type={User}
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
