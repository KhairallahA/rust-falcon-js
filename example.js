const { falconKeypair } = require('./src/index');

// Generate a random seed (48 bytes)
const seed_hex = 'e95afe2bfb5f361b4571e4de191d9af2de88d14ca3c34158fc9e9222746e986fa4ad4c577f80335d96f1c06a3db0e6b7';
const seed = new Uint8Array(Buffer.from(seed_hex, 'hex'));

// Generate a keypair
const keypair = falconKeypair(seed);
console.log('Generated keypair');

// Get public and secret keys
const publicKey = keypair.public;
const secretKey = keypair.secret;

console.log(`seed: ${seed}`);

console.log('Public key length:', publicKey.length);
console.log('Secret key length:', secretKey.length);
console.log('Public key:', Buffer.from(publicKey).toString('hex'));
// console.log('Secret key:', Buffer.from(secretKey).toString('hex'));
