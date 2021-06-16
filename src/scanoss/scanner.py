"""
 SPDX-License-Identifier: GPL-2.0-or-later

   Copyright (C) 2018-2021 SCANOSS LTD

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import json
import os
import sys

from .scanossapi import ScanossApi
from .winnowing import Winnowing

FILTERED_DIRS = {".git", ".svn", ".eggs", "__pycache__", ".metadata", ".idea",
                 ".sts4-cache", ".launch", ".vscode", ".vs", "venv", ".github", ".circleci"
                 "node_modules", "vendor"  # TODO should these be removed?
                 }
FILTERED_EXT = {  # File extensions
                ".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9", ".ac", ".adoc", ".am",
                ".asciidoc", ".bmp", ".build", ".cfg", ".chm", ".class", ".cmake", ".cnf",
                ".conf", ".config", ".contributors", ".copying", ".crt", ".csproj", ".css",
                ".csv", ".cvsignore", ".dat", ".data", ".doc", ".ds_store", ".dtd", ".dts",
                ".dtsi", ".dump", ".eot", ".eps", ".eslintignore", ".geojson", ".gdoc", ".gif", ".gitignore",
                ".gitattributes", ".glif", ".gmo", ".gradle", ".guess", ".hex", ".htm", ".html", ".ico", ".iml",
                ".in", ".inc", ".info", ".ini", ".ipynb", ".jpeg", ".jpg", ".json", ".jsonld", ".lock",
                ".log", ".m4", ".map", ".markdown", ".md", ".md5", ".meta", ".mk", ".mxml",
                ".o", ".otf", ".out", ".pbtxt", ".pdf", ".pem", ".phtml", ".plist", ".png",
                ".po", ".ppt", ".prefs", ".properties", ".pyc", ".qdoc", ".result", ".rgb",
                ".rst", ".scss", ".sha", ".sha1", ".sha2", ".sha256", ".sln", ".spec", ".sql",
                ".sub", ".svg", ".svn-base", ".tab", ".template", ".test", ".tex", ".tiff",
                ".toml", ".ttf", ".txt", ".utf-8", ".vim", ".wav", ".whl", ".woff", ".xht",
                ".xhtml", ".xls", ".xml", ".xpm", ".xsd", ".xul", ".yaml", ".yml", ".wfp",
                # File endings
                "-doc", "changelog", "config", "copying", "copying.lib", "license",
                "license.md", "license.txt", "licenses", "makefile", "notice",
                "readme", "swiftdoc", "texidoc", "todo", "version", "ignore"
                }
WFP_FILE_START = "file="
MAX_POST_SIZE = 64 * 1024  # 64k Max post size


class Scanner:
    """

    """
    def __init__(self, wfp: str = None, scan_output: str = None, output_format: str = 'plain',
                 debug: bool = False, trace: bool = False, quiet: bool = False, api_key: str = None, url: str = None,
                 sbom_path: str = None, scan_type: str = None, flags: str = None
                 ):
        """

        """
        self.quiet = quiet
        self.debug = debug
        self.trace = trace
        self.wfp = wfp if wfp else "scanner_output.wfp"
        self.scan_output = scan_output
        self.output_format = output_format
        self.winnowing = Winnowing(debug=debug, quiet=quiet)
        self.scanoss_api = ScanossApi(debug=debug, trace=trace, quiet=quiet, api_key=api_key, url=url,
                                      sbom_path=sbom_path, scan_type=scan_type, flags=flags
                                      )

    @staticmethod
    def __filter_files(files) -> list:
        """
        Filter which files should be considered for processing
        """
        file_list = []
        for f in files:
            ignore = False
            for ending in FILTERED_EXT:
                if f.lower().endswith(ending):
                    ignore = True
                    break
            if not ignore:
                file_list.append(f)
        return file_list

    @staticmethod
    def __strip_dir(scan_dir: str, length: int, path: str) -> str:
        """
        Strip the leading string from the specified path
        Parameters
        ----------
            scan_dir: str
                Root path
            length: int
                length of the root path string
            path: str
                Path to strip
        """
        if length > 0 and path.startswith(scan_dir):
            path = path[length:]
        return path

    @staticmethod
    def print_stderr(*args, **kwargs):
        """
        Print the given message to STDERR
        """
        print(*args, file=sys.stderr, **kwargs)

    @staticmethod
    def __count_files_in_wfp_file(wfp_file: str):
        """
        Count the number of files in the WFP that need to be processed
        Parameters
        ----------
            wfp_file: str
                WFP file to process
        """
        count = 0
        if wfp_file:
            with open(wfp_file) as f:
                for line in f:
                    if WFP_FILE_START in line:
                        count += 1
        return count

    def print_msg(self, *args, **kwargs):
        """
        Print message if quite mode is not enabled
        """
        if not self.quiet:
            self.print_stderr(*args, **kwargs)

    def print_debug(self, *args, **kwargs):
        """
        Print debug message if enabled
        """
        if self.debug:
            self.print_stderr(*args, **kwargs)

    def print_trace(self, *args, **kwargs):
        """
        Print trace message if enabled
        """
        if self.trace:
            self.print_stderr(*args, **kwargs)

    def __log_result(self, string, outfile=None):
        """
        Logs result to file or STDOUT
        """
        if not outfile and self.scan_output:
            outfile = self.scan_output
        if outfile:
            with open(outfile, "a") as rf:
                rf.write(string + '\n')
        else:
            print(string)

    def scan_folder(self, scan_dir: str):
        """
        Scan the specified folder producing fingerprints, send to the SCANOSS API and return results
        """
        if not scan_dir:
            raise Exception(f"ERROR: Please specify a folder to scan")
        if not os.path.exists(scan_dir) or not os.path.isdir(scan_dir):
            raise Exception(f"ERROR: Specified folder does not exist or is not a folder: {scan_dir}")
        wfps = ''
        scan_dir_len = len(scan_dir) if scan_dir.endswith(os.path.sep) else len(scan_dir)+1
        self.print_msg(f'Searching {scan_dir} for files to fingerprint...')
        for root, dirs, files in os.walk(scan_dir):
            dirs[:] = [d for d in dirs if d.lower() not in FILTERED_DIRS]  # skip directory if in the exclude list
            filtered_files = Scanner.__filter_files(files)                    # Strip out unwanted files
            self.print_trace(f'Root: {root}, Dirs: {dirs}, Files {filtered_files}')
            for file in filtered_files:
                path = os.path.join(root, file)
                file_stat = os.stat(path)
                if file_stat.st_size > 0:            # Ignore empty files
                    self.print_debug(f'Fingerprinting {path}...')
                    wfps += self.winnowing.wfp_for_file(path, Scanner.__strip_dir(scan_dir, scan_dir_len, path))
        if wfps:
            self.print_debug(f'Writing fingerprints to {self.wfp}')
            with open(self.wfp, 'w') as f:
                f.write(wfps)
            self.print_msg(f'Scanning fingerprints...')
            if self.scan_output:
                self.print_msg(f'Writing results to {self.scan_output}...')
            self.scan_wfp_file()
        else:
            Scanner.print_stderr(f'Warning: No files found to scan in folder: {scan_dir}')

    def scan_file(self, file: str):
        """
        Scan the specified file and produce a result
        Parameters
        ----------
            file: str
                File to fingerprint and scan/identify
        """
        if not file:
            raise Exception(f"ERROR: Please specify a file to scan")
        if not os.path.exists(file) or not os.path.isfile(file):
            raise Exception(f"ERROR: Specified files does not exist or is not a file: {file}")
        self.print_debug(f'Fingerprinting {file}...')
        wfps = self.winnowing.wfp_for_file(file, file)
        if wfps:
            self.print_debug(f'Scanning {file}...')
            if self.scan_output:
                self.print_msg(f'Writing results to {self.scan_output}...')
            self.scan_wfp(wfps)

    def scan_wfp_file(self, file: str = None):
        """
        Scan the contents of the specified WFP file
        Parameters
        ----------
            file: str
                WFP file to scan (optional)
        """
        wfp_file = file if file else self.wfp   # If a WFP file is specified, use it, otherwise us the default
        if not os.path.exists(wfp_file) or not os.path.isfile(wfp_file):
            raise Exception(f"ERROR: Specified WFP file does not exist or is not a file: {wfp_file}")
        file_count = Scanner.__count_files_in_wfp_file(wfp_file)
        cur_files = 0
        cur_size = 0
        batch_files = 0
        wfp = ''
        max_component = {'name': '', 'hits': 0}
        components = {}
        self.print_debug(f'Found {file_count} files to process.')
        raw_output = "{\n"
        file_print = ''
        with open(wfp_file) as f:
            for line in f:
                if line.startswith(WFP_FILE_START):
                    if file_print:
                        wfp += file_print         # Store the WFP for the current file
                        cur_size = len(wfp.encode("utf-8"))
                    file_print = line             # Start storing the next file
                    cur_files += 1
                    batch_files += 1
                else:
                    file_print += line             # Store the rest of the WFP for this file
                l_size = cur_size + len(file_print.encode('utf-8'))
                # Hit the max post size, so sending the current batch and continue processing
                if l_size >= MAX_POST_SIZE and wfp:
                    self.print_debug(f'Sending {batch_files} ({cur_files}) of'
                                     f' {file_count} ({len(wfp.encode("utf-8"))} bytes) files to the ScanOSS API.')
                    if cur_size > MAX_POST_SIZE:
                        Scanner.print_stderr(f'Warning: Post size {cur_size} greater than limit {MAX_POST_SIZE}')
                    scan_resp = self.scanoss_api.scan(wfp, max_component['name'])  # Scan current WFP and store
                    if scan_resp is not None:
                        for key, value in scan_resp.items():
                            raw_output += "  \"%s\":%s," % (key, json.dumps(value, indent=2))
                            for v in value:
                                if hasattr(v, 'get'):
                                    if v.get('id') != 'none':
                                        vcv = '%s:%s:%s' % (v.get('vendor'), v.get('component'), v.get('version'))
                                        components[vcv] = components[vcv] + 1 if vcv in components else 1
                                        if max_component['hits'] < components[vcv]:
                                            max_component['name'] = v.get('component')
                                            max_component['hits'] = components[vcv]
                                else:
                                    Scanner.print_stderr(f'Warning: Unknown value: {v}')
                    batch_files = 0
                    wfp = ''
        if file_print:
            wfp += file_print  # Store the WFP for the current file
        if wfp:
            self.print_debug(f'Sending {batch_files} ({cur_files}) of'
                             f' {file_count} ({len(wfp.encode("utf-8"))} bytes) files to the ScanOSS API.')
            scan_resp = self.scanoss_api.scan(wfp, max_component['name'])  # Scan current WFP and store
            first = True
            if scan_resp is not None:
                for key, value in scan_resp.items():
                    if first:
                        raw_output += "  \"%s\":%s" % (key, json.dumps(value, indent=2))
                        first = False
                    else:
                        raw_output += ",\n  \"%s\":%s" % (key, json.dumps(value, indent=2))
        raw_output += "\n}"
        if self.output_format == 'plain':
            self.__log_result(raw_output)
        elif self.output_format == 'cyclonedx':
            self.cyclonedx(raw_output)

    def scan_wfp(self, wfp: str):
        """
        Send the specified (single) WFP to ScanOSS for identification
        Parameters
        ----------
            wfp: str
                Winnowing Fingerprint to scan/identify
        """
        if not wfp:
            raise Exception(f"ERROR: Please specify a WFP to scan")
        raw_output = "{\n"
        scan_resp = self.scanoss_api.scan(wfp)
        if scan_resp is not None:
            for key, value in scan_resp.items():
                raw_output += "  \"%s\":%s" % (key, json.dumps(value, indent=2))
        raw_output += "\n}"
        if self.output_format == 'plain':
            self.__log_result(raw_output)
        elif self.output_format == 'cyclonedx':
            self.cyclonedx(raw_output)

    def wfp_file(self, scan_file: str, wfp_file: str = None):
        """
        Fingerprint the specified file
        """
        if not scan_file:
            raise Exception(f"ERROR: Please specify a file to fingerprint")
        if not os.path.exists(scan_file) or not os.path.isfile(scan_file):
            raise Exception(f"ERROR: Specified file does not exist or is not a file: {scan_file}")

        self.print_debug(f'Fingerprinting {scan_file}...')
        wfps = self.winnowing.wfp_for_file(scan_file, scan_file)
        if wfps:
            if wfp_file:
                self.print_stderr(f'Writing fingerprints to {wfp_file}')
                with open(wfp_file, 'w') as f:
                    f.write(wfps)
            else:
                print(wfps)
        else:
            Scanner.print_stderr(f'Warning: No fingerprints generated for: {scan_file}')

    def wfp_folder(self, scan_dir: str, wfp_file: str = None):
        """
        Fingerprint the specified folder producing fingerprints
        """
        if not scan_dir:
            raise Exception(f"ERROR: Please specify a folder to fingerprint")
        if not os.path.exists(scan_dir) or not os.path.isdir(scan_dir):
            raise Exception(f"ERROR: Specified folder does not exist or is not a folder: {scan_dir}")
        wfps = ''
        scan_dir_len = len(scan_dir) if scan_dir.endswith(os.path.sep) else len(scan_dir)+1
        self.print_msg(f'Searching {scan_dir} for files to fingerprint...')
        for root, dirs, files in os.walk(scan_dir):
            dirs[:] = [d for d in dirs if d.lower() not in FILTERED_DIRS]  # skip directory if in the exclude list
            filtered_files = Scanner.__filter_files(files)                    # Strip out unwanted files
            self.print_trace(f'Root: {root}, Dirs: {dirs}, Files {filtered_files}')
            for file in filtered_files:
                path = os.path.join(root, file)
                file_stat = os.stat(path)
                if file_stat.st_size > 0:            # Ignore empty files
                    self.print_debug(f'Fingerprinting {path}...')
                    wfps += self.winnowing.wfp_for_file(path, Scanner.__strip_dir(scan_dir, scan_dir_len, path))
        if wfps:
            if wfp_file:
                self.print_stderr(f'Writing fingerprints to {wfp_file}')
                with open(wfp_file, 'w') as f:
                    f.write(wfps)
            else:
                print(wfps)
        else:
            Scanner.print_stderr(f'Warning: No files found to fingerprint in folder: {scan_dir}')

    def cyclonedx(self, json_str: str):
        """

        """
        self.print_debug(f'Processing raw results into CycloneDX format...')
        results = json.loads(json_str)
        cdx = {}
        if results:
            for f in results:
                file_details = results.get(f)
                # print(f'File: {f}: {file_details}')
                for d in file_details:
                    id_details = d.get("id")
                    if not id_details or id_details == 'none':
                        # print(f'No ID for {f}')
                        continue
                    purl = None
                    purls = d.get('purl')
                    if not purls:
                        print(f'Purl block missing for {f}: {file_details}')
                        continue
                    for p in purls:
                        print(f'Purl: {p}')
                        purl = p
                        break
                    if not purl:
                        print(f'Warning: No PURL found for {f}: {file_details}')
                        continue
                    if cdx.get(purl):
                        print(f'Component {purl} already stored: {cdx.get(purl)}')
                        continue
                    fd = {}
                    print(f'Vendor: {d.get("vendor")}, Comp: {d.get("component")}, Ver: {d.get("version")},'
                          f' Latest: {d.get("latest")}')
                    for field in ['vendor', 'component', 'version', 'latest']:
                        fd[field] = d.get(field)
                    licenses = d.get('licenses')
                    for lic in licenses:
                        print(f'License: {lic.get("name")}')
                        fd['license'] = lic.get("name")
                        break
                    cdx[p] = fd
            print(f'License summary: {cdx}')

#
# End of ScanOSS Class
#