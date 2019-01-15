## simp-tpm12-rpms


## Description

This that builds and packages newer versions of TPM 1.2 simulator for testing
purposes.  It is a repackage of the upstream IBM's Software TPM 1.2 source code.

### This is a SIMP project

These module is a component of the [System Integrity Management
Platform][simp]
a compliance-management framework built on Puppet.

If you find any issues, they can be submitted to our
[JIRA][jira]or you can find us on

## Setup

To build rpm files to install the TPM 1.2 simulator, install this
package and update the configuration files, namely `things_to_build.yaml`
and `simp-tpm12-simulator.spec` as necessary.  Then build and package
simulator with the command `bundle exec rake pkg:rpm` from with the
simp-tpm12-simulator directory.

### Beginning with simp-tpm12-rpm

## Usage

To install the rpm, copy the rpm file to the target system and install it
with the command:

```yaml
yum localinstall simp-tpm12-simulator-*.rpm
```

This will install the simulator programs, utilities, and servics necessary
to start and utilize the TPM 1.2 simulator.

To initialize and use the TPM simulator, issue the following commands:

```yaml
# systemctl start tpm12-simulator
# systemctl start tpm12-tpmbios
# systemctl restart tpm12-simulator
# systemctl start tpm12-tpmbios
# systemctl start tpm12-tpminit
# systemctl start tpm12-tcsd
```


[simp]: https://github.com/NationalSecurityAgency/SIMP/
[jira]: https://simp-project.atlassian.net/
