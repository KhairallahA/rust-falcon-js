const { falconKeypair } = require('./src/index');

// Generate a random seed (48 bytes)
const seed = new Uint8Array(48);
crypto.getRandomValues(seed);

// Generate a keypair
const keypair = falconKeypair(seed);
console.log('Generated keypair');

// Get public and secret keys
const publicKey = keypair.public;
const secretKey = keypair.secret;

console.log('Public key length:', publicKey.length);
console.log('Secret key length:', secretKey.length);
