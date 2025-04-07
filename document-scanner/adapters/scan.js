const util = require('util');
const path = require('path');
const exec = util.promisify(require('child_process').exec);
const log = require('loglevel');


const NO_RECTANGLE_DETECTED_ERROR = "name 'screenCnt' is not defined";

class DocumentScanner {
  static async scan(filePath, outputFolderPath) {
    const commandPrefix = process.env.LAMBDA_TASK_ROOT ? '' : 'pipenv run ';
    // const commandPrefix = 'pipenv run ';
    // const executablePath = '../scan.py';
    const executablePath = path.join(process.env.LAMBDA_TASK_ROOT || '../', './scan.py');
    const outputFilePath = path.join(outputFolderPath, `scan${path.extname(filePath)}`);

    const { stdout, stderr } = await exec(`cd ${__dirname}; ${commandPrefix} python ${executablePath} -i ${filePath} -o ${outputFilePath}`);
    if (stderr) {
      return Promise.reject(stderr);
    }
    log.info(stdout);

    return Promise.resolve(outputFilePath);
  }
}

module.exports = DocumentScanner;
