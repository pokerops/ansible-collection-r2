# pokerops.r2

[![Build Status](https://github.com/pokerops/ansible-collection-r2/actions/workflows/molecule.yml/badge.svg)](https://github.com/pokerops/ansible-collection-r2/actions/wofklows/molecule.yml)
[![Ansible Galaxy](http://img.shields.io/badge/ansible--galaxy-pokerops.r2.vim-blue.svg)](https://galaxy.ansible.com/pokerops/r2/)

<!--
[![Ansible Galaxy](https://img.shields.io/badge/dynamic/json?color=blueviolet&label=pokerops/r2&query=%24.summary_fields.versions%5B0%5D.name&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2F<galaxy_id>%2F%3Fformat%3Djson)](https://galaxy.ansible.com/pokerops/r2/)
 -->

An [ansible role](https://galaxy.ansible.com/ui/repo/published/pokerops/r2/) to create and configure Cloudflare R2 buckets

## Collection Variables

| Parameter                     | Default | Type    | Description                          | Required |
| :---------------------------- | ------: | :------ | :----------------------------------- | :------- |
| r2_access_key_id              |     n/a | string  | Cloudflare R2 access key ID          | yes      |
| r2_secret_access_key          |     n/a | string  | Cloudflare R2 secret access key ID   | yes      |
| r2_account_id                 |     n/a | string  | Cloudflare R2 account ID             | yes      |
| r2_cloudflare_email           |     n/a | string  | Cloudflare email address             | yes      |
| r2_cloudflare_api_token       |     n/a | string  | Cloudflare API token                 | yes      |
| r2_buckets                    |      [] | list    | Cloudflare R2 buckets                | yes      |
| r2_region                     |    auto | string  | Cloudflare R2 region                 | no       |
| r2_hostgroup                  |      r2 | string  | Cloudflare R2 ansible hostgroup name | no       |
| r2_cloudflare_control_retries |       2 | integer | Cloudflare R2 task retries           | no       |
| r2_cloudflare_control_delay   |     120 | integer | Cloudflare R2 task delay             | no       |
| r2_buckets_ignore             |      [] | list    | Cloudflare R2 buckets ignore list    | no       |
| r2_object_sync_timeout        |    1200 | integer | Cloudflare R2 object sync timeout    | no       |
| r2_object_sync_delay          |      20 | integer | Cloudflare R2 object sync delay      | no       |

## Collection playbooks

- pokerops.r2.install: Install, modify and delete Cloudflare R2 buckets
- pokerops.r2.sync: Sync objects into Cloudflare R2 buckets

## Testing

Please make sure your environment has [docker](https://www.docker.com) installed in order to run role validation tests. Additional python dependencies are listed in the [requirements file](https://github.com/nephelaiio/ansible-role-requirements/blob/master/requirements.txt)

Collection is tested against the following distributions (docker images):

- Ubuntu Jammy
- Debian Bookworm

You can test the role directly from sources using command `make test`

## License

This project is licensed under the terms of the [MIT License](https://opensource.org/license/mit)
