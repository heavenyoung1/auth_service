module.exports = {
  testEnvironment: 'jsdom',
  setupFiles: ['jest-fetch-mock'],
  setupFilesAfterEnv: ['./setupTests.js'],
  transform: {
    '^.+\\.jsx?$': 'babel-jest',
    '^.+\\.mjs$': 'babel-jest',
  },
  moduleNameMapper: {
    '\\.(css|less|scss)$': 'identity-obj-proxy'
  }
};