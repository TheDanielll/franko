/**
 * Uses esbuild to bundle the CLI script (decline.js) and its dependencies
 * into a single file for distribution and use in a Node.js 14 environment.
 */

require('esbuild').buildSync({
  // The entry point for the bundle (our CLI tool)
  entryPoints: ['decline.js'],

  // Bundle all imported modules into the output file
  bundle: true,

  // Target the Node.js runtime (not browser)
  platform: 'node',

  // Specify the minimum Node.js version compatibility
  target: ['node14'],

  // The output file that will contain the bundled code
  outfile: 'decline.bundle.js',
});
