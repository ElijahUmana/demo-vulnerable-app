# DeepSentinel Security Rules

## Security
- Flag any function that handles user input without sanitization
- Flag any SQL query built with string concatenation or f-strings
- Flag any use of os.system(), subprocess with shell=True, or eval()
- Flag any hardcoded credentials, API keys, or passwords
- Flag any use of MD5 or SHA1 for password hashing
- Flag any HTTP (non-HTTPS) URLs in production code
- Flag any deserialization of untrusted data (pickle, yaml.load, eval)
- Flag any file operations with user-controlled paths lacking validation

## Style
- All API endpoints must validate input types before processing
- Database queries must use parameterized queries, never string formatting
- Error responses must not expose internal paths, stack traces, or environment variables
