# FirebaseDigitsServer
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

```swift
import Foundation
import DigitsKit

class TokenManager {
    static let baseURL = "URL_HERE"
    static let tokenPath = "token"
    
    static let operationQueue = NSOperationQueue()
    
    static func generateToken(session: DGTSession, callback: (token: String?, error: NSError?)->()) {
        generateToken(session.authToken, auth_token_secret: session.authTokenSecret, callback: callback)
    }
    
    static func generateTokenURL(auth_token: String, auth_token_secret: String) -> NSURL {
        let urlString = NSString(format: "%@%@?auth_token=%@&auth_token_secret=%@", baseURL, tokenPath, auth_token, auth_token_secret) as String!
        return NSURL(string: urlString)!
    }
    
    static func generateToken(auth_token: String, auth_token_secret: String, callback: (token: String?, error: NSError?)->()) {
        // Generate URL
        let url = generateTokenURL(auth_token, auth_token_secret: auth_token_secret)
        
        let task = NSURLSession.sharedSession().dataTaskWithURL(url, completionHandler: { (data, response, error) in
            if (data != nil && error == nil) {
                let responseString = NSString(data: data!, encoding: NSUTF8StringEncoding)
                
                // Chech for invalid
                if responseString == "invalid" {
                    // Return error
                    callback(token: nil, error: NSError(domain: "DOMAIN_HERE", code: 1, userInfo: [
                        NSLocalizedDescriptionKey :  "Invalid authorization token",
                        ]))
                    return
                } else {
                    // Send token as response
                    callback(token: responseString! as String, error: nil)
                }
            } else {
                callback(token: nil, error: error)
                return
            }
        })
        
        // Start request
        task.resume()
    }
}
```
