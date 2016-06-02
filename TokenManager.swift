import Foundation
import DigitsKit

class TokenManager {
    static let baseURL = "***REMOVED***"
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
                var json: NSDictionary?
                do {
                    json = try NSJSONSerialization.JSONObjectWithData(data!, options: []) as? NSDictionary
                } catch {
                    callback(token: nil, error: standardError())
                    return
                }
                
                // Chech for invalid
                if let error = json!["error"] as? String {
                    // Return error
                    callback(token: nil, error: standardError())
                    return
                } else {
                    // Send token as response
                    callback(token: json!["token"] as! String, error: nil)
                }
            } else {
                callback(token: nil, error: error)
                return
            }
        })
        
        // Start request
        task.resume()
    }
    
    private static func standardError() -> NSError {
        return NSError(domain: "DOMAIN_HERE", code: 1, userInfo: [
            NSLocalizedDescriptionKey :  "Invalid authorization token",
            ])
    }
}
