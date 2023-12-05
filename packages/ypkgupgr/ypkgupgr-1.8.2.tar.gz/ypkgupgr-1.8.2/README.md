# ypkgupgr
## The pip package updater by yesseruser

This is a package updater that updates all outdated packages when run.  

To install, follow the steps listed here:  
[Installation](https://github.com/yesseruser/ypkgupgr/wiki/Installation)

Here's the wiki page:  
[Wiki](https://github.com/yesseruser/ypkgupgr/wiki)

If you're running the package from a python file, please **use a subprocess** instead of importing and calling the `update_packages` function. This is because the package can update itself and can result in an error because of the code changing.
## What's Changed
* Fixed package names showing in previously set color by @yesseruser in https://github.com/yesseruser/ypkgupgr/pull/2

## New Contributors
* @yesseruser made their first contribution in https://github.com/yesseruser/ypkgupgr/pull/2

**Full Changelog**: https://github.com/yesseruser/ypkgupgr/compare/1.8.1...1.8.2
