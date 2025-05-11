// build.js
require('esbuild').buildSync({
  entryPoints: ['decline.js'],
  bundle: true,
  platform: 'node',
  target: ['node14'],
  outfile: 'decline.bundle.js',
});