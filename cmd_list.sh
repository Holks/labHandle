# authorise API use
response=$(http --auth <user>:<pass> POST http://localhost:5000/api/tokens)
echo "Authentication retrieval response $response"
if [[ $response = *"token"* ]]; then
  echo "Token found!"
  IFS=':' read -ra token <<< "$response"
  echo ${token[1]}
  token=${token[1]:1:-2}
  echo $token
fi
# get list of users
users=$(http GET http://localhost:5000/api/users name=admin "Authorization:Bearer $token")
echo $users

