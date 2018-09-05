pipeline {
  agent any
  stages {
    stage('Checking out source code') {
      steps {
        git(url: 'https://github.com/input-output-hk/theseus', branch: '*/master', changelog: true, credentialsId: 'IOHK-QA', poll: true)
      }
    }
    stage('Assign Version Number') {
      steps {
        sh '''# patch in the build number
perl -pi -e "s/Source/$BUILD_NUMBER/" Theseus/version.py'''
      }
    }
    stage('Install dependencies') {
      steps {
        sh '''# ensure we have all the specified dependencies upto date
pip3.7 install -e . --user --upgrade'''
      }
    }
    stage('Run unit tests') {
      steps {
        sh '''# run the tests with xunit output
python3.7 /usr/bin/nosetests3 --with-xunit --xunit-file nosetests.xml --xunit-testsuite-name=Theseus -d --verbosity 2 -w Theseus/Tests/
'''
      }
    }
    stage('Build egg file') {
      steps {
        sh '''echo "Building egg file"
python3.7 setup.py bdist_egg

echo "copying egg file"
cp dist/theseus*.egg theseus.egg'''
      }
    }
    stage('Build and Publish documentation') {
      steps {
        sh '''cd sphinx
make html'''
      }
    }
    stage('Archive artifacts') {
      steps {
        archiveArtifacts 'theseus.egg, nosetests.xml theseus.log'
      }
    }
    stage('Publish test results') {
      steps {
        junit(testResults: '**/nosetests.xml', keepLongStdio: true)
      }
    }
  }
}