# Firebase Digits Server
A server for Google App Engine to generate authentication tokens for Firebase from digits responses

## How to Use
#### Server
1. Create a new Google App Engine Project
2. Add a service account with a JSON key
3. Paste the email address and key from that in config.yaml
4. Get your twitter authentication info from your Info.plist file (Fabric->Kits[i]->KitInfo) and paste that into config.yaml
5. Copy app.example.yaml to app.yaml and fill in your application name
6. Deploy

#### App
1. In your -digitsAuthenticationFinishedWithSession:error: callback, make a request to the server with the following parameters:
  * auth_token
  * auth_token_secret
2. Use the response and call -signInWithCustomToken:completion: with the token returned from the server
```swift
TokenManager.generateToken(session, callback: { (token, error) in
  FIRAuth.auth()?.signInWithCustomToken(self.token!, completion: nil)
})
```
