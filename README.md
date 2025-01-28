# Lapine-Secreter
Generates .env secrets from a secret request file (.secreq).

## Usage

```
lapine-secreter.py [mode] [/path/to/file.secreq]
```

The 'generate-env' mode will generate a .env file following the rules defined in the 'Request File Format' section. This will also overwrite any 'overwrites' in place and move them to a '.bak' file.

The 'revert' mode will restore and '.bak' overwrites file to the original file. 

## Request File Format

Each line of a secret request file (.secreq) contains a key value pair written to the '.env' output.
The following codeblock demonstrates the secret request format. 
```
[key]: [format] [format_arg] <overwrites [file1] [file2] [file3]> 
```
The following formats with their args are provided:
| Format | Format argument | Default | 
| -- | -- | -- |
|literal | The literal value to place in the output until the end of the line.| NULL | 
|hex | Length in characters. | 32  |
|urlsafe | Length in characters. |32 |

The 'overwrites' keyword can be used to specify an inplace replacement for literal text matches in files. Paths should be relative from where the binary is being called, ideally the project root. Created files are saved in place, with the originals moved to '.bak'. This is a potentially destructive action and can be reverted with the 'revert' mode.
