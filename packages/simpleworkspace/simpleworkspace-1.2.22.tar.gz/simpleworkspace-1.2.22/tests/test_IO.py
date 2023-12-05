import hashlib
import os
import simpleworkspace.loader as sw
from simpleworkspace.io.path import PathInfo
from basetestcase import BaseTestCase
from simpleworkspace.io.readers.csvreader import CSVReader

class IOTests(BaseTestCase):
    class _tmpNestedFolderInfo():
        SubEntriesCount = 0
        SubDirCount = 0
        FileCount = 0
        FileOfTypeTextCount = 0
        FileOfTypeTextContent = ''
        FileOfTypeBinaryCount = 0
        FileOfTypeBinaryContent = b''
        totalFileSize = 0
        entryPath = ""

    def _tmpNestedFolder(self):
        nestedInfo = self._tmpNestedFolderInfo()
        nestedInfo.entryPath = self.tmpDir("nested")
        nestedInfo.FileOfTypeBinaryContent = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"
        nestedInfo.FileOfTypeTextContent = "1234567890"

        self.tmpDir(f"./nested/a1")
        self.tmpFile("nested/a1/file1.txt", nestedInfo.FileOfTypeTextContent)
        self.tmpFile("nested/a1/file2.txt", nestedInfo.FileOfTypeTextContent)
        self.tmpFile("nested/a1/file3.bin",  nestedInfo.FileOfTypeBinaryContent)
        self.tmpDir(f"./nested/a1/a2")
        self.tmpDir(f"./nested/a1/a2/a3")
        self.tmpDir(f"./nested/b1")
        self.tmpDir(f"./nested/c1/a2")
        self.tmpDir(f"./nested/c1/b2")
        self.tmpDir(f"./nested/c1/c2")
        self.tmpDir(f"./nested/c1/c2/c3")
        self.tmpDir(f"./nested/c1/c2/c3/c4")
        self.tmpFile("nested/c1/c2/c3/c4/file1.txt", nestedInfo.FileOfTypeTextContent)
        self.tmpFile("nested/c1/c2/c3/c4/file2.bin",  nestedInfo.FileOfTypeBinaryContent)
        nestedInfo.SubDirCount = 10
        nestedInfo.FileOfTypeBinaryCount = 2
        nestedInfo.FileOfTypeTextCount = 3
        nestedInfo.FileCount = nestedInfo.FileOfTypeBinaryCount + nestedInfo.FileOfTypeTextCount
        nestedInfo.totalFileSize = len(nestedInfo.FileOfTypeBinaryContent) * nestedInfo.FileOfTypeBinaryCount + len(nestedInfo.FileOfTypeTextContent) * nestedInfo.FileOfTypeTextCount
        nestedInfo.SubEntriesCount = nestedInfo.SubDirCount + nestedInfo.FileCount
        return nestedInfo

    def test_CSVReader_ReadingAndSaving(self):
        tmpFilepath = self.tmpFile('tmp.csv')
        
        csv = CSVReader(delimiter=',')
        csv.Headers = ["col1", "col2"]
        csv.Rows.append(["1", "2"])
        csv.Rows.append(["3", "4"])
        csv.Save(tmpFilepath)

        data = sw.io.file.Read(tmpFilepath)
        self.assertEqual(
            data,
            "col1,col2\n" +
            "1,2\n" +
            "3,4\n"
        )

        csv = CSVReader(delimiter=',')
        csv.Load(tmpFilepath, hasHeader=True)
        self.assertEqual(
            csv.Headers,
            ["col1", "col2"]
        )
        self.assertEqual(
            csv.Rows,
            [
                ["1", "2"],
                ["3", "4"]
             ]
        )

        csv.Headers = []
        csv.Rows[0][1] = "20"
        csv.Save(tmpFilepath)

        data = sw.io.file.Read(tmpFilepath)
        self.assertEqual(
            data,
            "1,20\n" +
            "3,4\n"
        )

        csv = CSVReader(delimiter=',')
        csv.Load(tmpFilepath, hasHeader=False)
        self.assertEqual(
            csv.Headers,
            []
        )
        self.assertEqual(
            csv.Rows,
            [
                ["1", "20"],
                ["3", "4"]
             ]
        )
        
        return
    

    def test_FileReader_HasCorrectTypes(self):
        f1 = self.tmpFile("file1.txt", "1234567890")
            
        data = sw.io.file.Read(f1)
        self.assertIs(type(data), str)

        data = sw.io.file.Read(f1, type=bytes)
        self.assertIs(type(data), bytes)

        with self.assertRaises(TypeError):
            data = sw.io.file.Read(f1, type=list)


    def test_FileReader_Iterator_HasCorrectTypes(self):
        f1 = self.tmpFile("file1.txt", "1234567890")
            
        for data in sw.io.file.ReadIterator(f1, 10):
            self.assertIs(type(data), str)

        for data in sw.io.file.ReadIterator(f1, 10, type=bytes):
            self.assertIs(type(data), bytes)

        with self.assertRaises(TypeError):
            for data in sw.io.file.ReadIterator(f1, 10, type=list):
                pass

    def test_FileReader_ReadsCorrect(self):
        #empty file test
        f1 = self.tmpFile("empty.txt", "")
        self.assertEqual(sw.io.file.Read(f1), "")
        self.assertEqual(sw.io.file.Read(f1, type=bytes), b"")

        #simple reads
        fileContent = "1234567890"
        f1 = self.tmpFile("file1.txt", fileContent)
        result = sw.io.file.Read(f1, readLimit=len(fileContent))
        self.assertEqual(result,  fileContent)
        dataBytes = sw.io.file.Read(f1, readLimit=len(fileContent), type=bytes)
        self.assertEqual(dataBytes,  fileContent.encode())
        
        #readlimit shorter than filesize
        result = sw.io.file.Read(f1, readLimit=2)
        self.assertEqual(result, "12")
        result = sw.io.file.Read(f1, readLimit=0)
        self.assertEqual(result, "")

      

    def test_FileReader_Iterator_ReadsCorrect(self):
        #empty file test
        testfile = self.tmpFile("empty.txt", "")
        chunksRead = list(sw.io.file.ReadIterator(testfile, 10))
        self.assertEqual(chunksRead, [])
        chunksRead = list(sw.io.file.ReadIterator(testfile, 10, type=bytes))
        self.assertEqual(chunksRead, [])

        fileContent = "1234567890"
        testfile = self.tmpFile("file1.txt", fileContent)

        #scenario readsize larger than filesize
        chunksRead = list(sw.io.file.ReadIterator(testfile, readSize=100))
        self.assertEqual(chunksRead, ["1234567890"])

        # scenario has readSize smaller than readlimit
        chunksRead = list(sw.io.file.ReadIterator(testfile, readSize=2, readLimit=6))
        self.assertEqual(chunksRead, ["12", "34", "56"])
        
        # scenerio has only readsize, should read unlimited
        chunksRead = list(sw.io.file.ReadIterator(testfile, readSize=2))
        self.assertEqual(
            chunksRead,
            ["12", "34", "56", "78", "90"]
        )

        #scenario has readsize bigger than readlimit, should only be able to read until readlimit
        chunksRead = list(sw.io.file.ReadIterator(testfile, readSize=5, readLimit=2))
        self.assertEqual(chunksRead, ["12"])

        # scenario has readSize is equal to readlimit, should therefor read once
        chunksRead = list(sw.io.file.ReadIterator(testfile, readSize=2, readLimit=2))
        self.assertEqual(chunksRead, ["12"])

    def test_Hash_GetsCorrectHash(self):
        fileContent = b"\x00\x01\x02\x03\x04"
        f1 = self.tmpFile("file1.txt", fileContent)
        originalHash = sw.io.file.Hash(f1, hashFunc=hashlib.sha256())

        #
        sha256 = hashlib.sha256()
        sha256.update(fileContent)
        resultHash = sha256.hexdigest()
        self.assertEqual(originalHash,  resultHash)
        #
        sha256 = hashlib.sha256()
        sha256.update(sw.io.file.Read(f1, type=bytes))
        resultHash = sha256.hexdigest()
        self.assertEqual(originalHash,  resultHash)
        #
        sha256 = hashlib.sha256()
        for chunk in sw.io.file.ReadIterator(f1, readSize=2, type=bytes):
            sha256.update(chunk)
        resultHash = sha256.hexdigest()
        self.assertEqual(originalHash,  resultHash)
        #
        sha256 = hashlib.sha256()
        for chunk in sw.io.file.ReadIterator(f1, readSize=len(fileContent), readLimit=len(fileContent), type=bytes):
            sha256.update(chunk)
        resultHash = sha256.hexdigest()
        self.assertEqual(originalHash, resultHash)


    def test_Directories_ListsAll(self):
        nestedInfo = self._tmpNestedFolder()
        
        fileSizes = []
        for path in sw.io.directory.Scan(nestedInfo.entryPath, includeDirs=False):
            fileSizes.append(os.path.getsize(path))
        self.assertEqual(sum(fileSizes),  nestedInfo.totalFileSize)

        #
        tmpList = list(sw.io.directory.Scan(nestedInfo.entryPath, includeDirs=False))
        self.assertEqual(len(tmpList),  nestedInfo.FileCount)

        #
        tmpList = list(sw.io.directory.Scan(nestedInfo.entryPath, includeDirs=True))
        self.assertEqual(len(tmpList),  nestedInfo.SubEntriesCount)
        return

    def test_Directories_ListsOnlyDirectories(self):
        nestedInfo = self._tmpNestedFolder()

        #
        tmpList = list(sw.io.directory.Scan(nestedInfo.entryPath, includeDirs=False, includeFiles=False))
        self.assertEqual(len(tmpList),  0)

        #
        tmpList = list(sw.io.directory.Scan(nestedInfo.entryPath, includeDirs=True, includeFiles=False))
        self.assertEqual(len(tmpList),  nestedInfo.SubDirCount)

    def test_Directories_ListsAll_maxDepth(self):
        nestedInfo = self._tmpNestedFolder()
        #
        level1_Entries = list(os.scandir(nestedInfo.entryPath)) 
        totalEntriesLevel1 = len(level1_Entries)

        tmpList = list(sw.io.directory.Scan(nestedInfo.entryPath, maxRecursionDepth=1))
        self.assertEqual(len(tmpList),  totalEntriesLevel1)

        level2_Entries = []
        totalEntriesLevel2 = totalEntriesLevel1
        for fd in level1_Entries:
            if(fd.is_dir()):
                entries = list(os.scandir(fd.path))
                level2_Entries.extend(entries)
                totalEntriesLevel2 += len(entries)

        tmpList = list(sw.io.directory.Scan(nestedInfo.entryPath, maxRecursionDepth=2))
        self.assertEqual(len(tmpList),  totalEntriesLevel2)

        level3_Entries = []
        totalEntriesLevel3 = totalEntriesLevel2
        for fd in level2_Entries:
            if(fd.is_dir()):
                entries = list(os.scandir(fd.path))
                level3_Entries.extend(entries)
                totalEntriesLevel3 += len(entries)
        
        tmpList = list(sw.io.directory.Scan(nestedInfo.entryPath, maxRecursionDepth=3))
        self.assertEqual(len(tmpList),  totalEntriesLevel3)


        tmpList = list(sw.io.directory.Scan(nestedInfo.entryPath, includeDirs=False, maxRecursionDepth=9999))
        self.assertEqual(len(tmpList),  nestedInfo.FileCount)

        allItems = list(sw.io.directory.Scan(nestedInfo.entryPath, maxRecursionDepth=9999))
        self.assertEqual(len(allItems),  nestedInfo.SubEntriesCount)
        return


    def test_Directories_callbackFiltering_1(self):
        nestedInfo = self._tmpNestedFolder()
        tmpList = list(sw.io.directory.Scan(nestedInfo.entryPath, filter = lambda x: x.endswith(".txt") or x.endswith(".unknown")))
        
        self.assertEqual(len(tmpList), nestedInfo.FileOfTypeTextCount)
        for i in tmpList:
            pi = PathInfo(i)
            self.assertEqual(pi.FileExtension, "txt")
        return

    def test_Directories_regexFiltering_1(self):
        nestedInfo = self._tmpNestedFolder()

        tmpList = list(sw.io.directory.Scan(nestedInfo.entryPath, filter=r"/\.(unkown|txt)/i"))
        self.assertEqual(len(tmpList), nestedInfo.FileOfTypeTextCount)
        for i in tmpList:
            pi = PathInfo(i)
            self.assertEqual(pi.FileExtension, "txt")
        return

    def test_Directories_regexFiltering_2(self):
        nestedInfo = self._tmpNestedFolder()

        tmpList = list(sw.io.directory.Scan(nestedInfo.entryPath, filter=r"/\.(bin)$/i"))
        for path in tmpList:
            self.assertEqual(
                sw.io.file.Read(path, type=bytes),
                nestedInfo.FileOfTypeBinaryContent
            )
        self.assertEqual(len(tmpList),  nestedInfo.FileOfTypeBinaryCount)

    def test_Directories_regexFiltering_3(self):
        nestedInfo = self._tmpNestedFolder()
        tmpList = list(sw.io.directory.Scan(nestedInfo.entryPath, filter=r"/\.(unkown)$/"))
        self.assertEqual(len(tmpList),  0)
        return

    def test_Directories_regexFiltering_AllFiles_1(self):
        nestedInfo = self._tmpNestedFolder()
        tmpList = list(sw.io.directory.Scan(nestedInfo.entryPath, filter=r"/\.(bin|txt)$/"))
        self.assertEqual(len(tmpList),  nestedInfo.FileCount)
        return

    def test_Directories_regexFiltering_AllFiles_2(self):
        nestedInfo = self._tmpNestedFolder()
        tmpList = list(sw.io.directory.Scan(nestedInfo.entryPath, filter=r"/.*/i"))
        self.assertEqual(len(tmpList),  nestedInfo.SubEntriesCount)


    def test_Directories_files_in_directory(self):
        tmpdir = self.tmpDir("a")
        file1 = self.tmpFile("a/file1.txt")
        file2 = self.tmpFile("a/file2.txt")
        file3 = self.tmpFile("a/file3.jpg")

        # Test listing files
        files = list(sw.io.directory.Scan(tmpdir))
        self.assertEqual(len(files), 3)
        self.assertIn(file1, files)
        self.assertIn(file2, files)
        self.assertIn(file3, files)

    def test_Directories_directories_in_directory(self):
        # Create a temporary directory and some subdirectories

        entryDir = self.tmpDir("a")
        subDir1 = self.tmpDir("a/dir1")
        subDir2 = self.tmpDir("a/dir2")

        # Test listing directories
        dirs = list(sw.io.directory.Scan(entryDir, includeDirs=True, includeFiles=False))
        self.assertEqual(len(dirs), 2)
        self.assertIn(subDir1, dirs)
        self.assertIn(subDir2, dirs)


    def test_Directories_include_filter(self):
        # Create a temporary directory and some files
        tmpdir = self.tmpDir("a")
        file1 = self.tmpFile("a/file1.txt")
        file2 = self.tmpFile("a/file2.txt")
        file3 = self.tmpFile("a/file3.jpg")

        # Test filtering files by extension
        files = list(sw.io.directory.Scan(tmpdir, filter=r'/\.txt$/'))
        self.assertEqual(len(files), 2)
        self.assertIn(file1, files)
        self.assertIn(file2, files)
        self.assertNotIn(file3, files)
        return
    
    def test_Directories_earlyExits(self):
        # Create a temporary directory and some files
        tmpdir = self.tmpDir("a1/")
        self.tmpDir("a1/a2/")
        nestedFile = self.tmpFile("a1/a2/nestedFile.txt")

        file1 = self.tmpFile("a1/file1.txt")
        file2 = self.tmpFile("a1/file2.txt")
        file3 = self.tmpFile("a1/file3.jpg")

        # Test stopping recursion early with a satisfied condition
        files = []
        for path in sw.io.directory.Scan(tmpdir):
            files.append(path)
            if('file2.txt' in path):
                break
        self.assertIn(file2, files)
        self.assertNotIn(nestedFile, files)

        # Test satisfied condition with everything allowed through
        files = []
        for path in sw.io.directory.Scan(tmpdir):
            files.append(path)
        self.assertEqual(len(files), 5)
        self.assertIn(file1, files)
        self.assertIn(file2, files)
        self.assertIn(file3, files)
        self.assertIn(nestedFile, files)

        # Test exiting right away directly
        hitCounter = 0
        for path in sw.io.directory.Scan(tmpdir):
            hitCounter += 1
            break
        self.assertEqual(hitCounter, 1)
        return

    def test_PathInfo_GetsValidPaths(self):
        t0 = PathInfo("/a/b/c.exe")
        t1 = PathInfo("a/b/c.exe")
        t2 = PathInfo("a/b/c")
        t3 = PathInfo("a/b/.exe")
        t4 = PathInfo(".exe")
        t5 = PathInfo("c")
        t6 = PathInfo("c.exe")
        t7 = PathInfo(".")
        t8 = PathInfo("a.,-.asd/\\/b.,ca.asd/c.,..exe")
        
        self.assertTrue(t0.FileExtension == "exe" and t0.Filename == "c"    and t0.Tail == "/a/b"                  and t0.Head == "c.exe"     )
        self.assertTrue(t1.FileExtension == "exe" and t1.Filename == "c"    and t1.Tail == "a/b"                   and t1.Head == "c.exe"     )
        self.assertTrue(t2.FileExtension == ""    and t2.Filename == "c"    and t2.Tail == "a/b"                   and t2.Head == "c"         )
        self.assertTrue(t3.FileExtension == "exe" and t3.Filename == ""     and t3.Tail == "a/b"                   and t3.Head == ".exe"      )
        self.assertTrue(t4.FileExtension == "exe" and t4.Filename == ""     and t4.Tail == ""                      and t4.Head == ".exe"      )
        self.assertTrue(t5.FileExtension == ""    and t5.Filename == "c"    and t5.Tail == ""                      and t5.Head == "c"         )
        self.assertTrue(t6.FileExtension == "exe" and t6.Filename == "c"    and t6.Tail == ""                      and t6.Head == "c.exe"     )
        self.assertTrue(t7.FileExtension == ""    and t7.Filename == ""     and t7.Tail == ""                      and t7.Head == "."         )
        self.assertTrue(t8.FileExtension == "exe" and t8.Filename == "c.,." and t8.Tail == "a.,-.asd///b.,ca.asd"  and t8.Head == "c.,..exe"  )

        return

    def test_PathInfo_Traverse(self):
        t0 = PathInfo("/d1/d2/leaf.txt")
        self.assertTrue(t0.Tail == "/d1/d2" and t0.Head == "leaf.txt")
        self.assertTrue(t0.Parent.Tail == "/d1" and t0.Parent.Head == "d2")
        self.assertTrue(t0.Parent.Parent.Tail == "/" and t0.Parent.Parent.Head == "d1")
        
        t1 = t0.Parent / "d3" / t0.Head
        self.assertTrue(t1.Tail == "/d1/d2/d3" and t1.Head == "leaf.txt")
        t2 = t0.Parent.Join("d3").Join(t0.Head)
        self.assertTrue(t2.Tail == "/d1/d2/d3" and t2.Head == "leaf.txt")



    def test_PathInfo_UsesCaching(self):
        t0 = PathInfo("a/b/c.exe")
        self.assertTrue(t0.Filename is t0.Filename)
        self.assertTrue(t0.FileExtension is t0.FileExtension)
        self.assertTrue(t0.Tail is t0.Tail)
        self.assertTrue(t0.Head is t0.Head)
        self.assertTrue(t0.AbsolutePath is t0.AbsolutePath)
        self.assertTrue(t0._HeadTail is t0._HeadTail)
        self.assertTrue(t0._FilenameSplit is t0._FilenameSplit)
        return
    
    def test_PathInfo_NormalizeFlag(self):
        pInfo = PathInfo("a\\b\\c.exe")
        self.assertEqual("a/b/c.exe", pInfo.Path)
        self.assertTrue("a/b/c.exe" in pInfo.AbsolutePath)

        pInfo = PathInfo("a\\b\\c.exe", normalizePath=False)
        self.assertEqual("a\\b\\c.exe", pInfo.Path)
        self.assertTrue("a\\b\\c.exe" in pInfo.AbsolutePath)

    def test_PathInfo_HelperMethods(self):
        pInfo = PathInfo(self.testPath +  "/newDirectory")
        self.assertEqual(pInfo.Exists, False)
        self.assertEqual(pInfo.IsDirectory, False)
        self.assertEqual(pInfo.IsFile, False)
        self.assertEqual(pInfo.IsSymlink, False)

        pInfo.CreateDirectory()
        self.assertEqual(pInfo.Exists, True)
        self.assertEqual(pInfo.IsDirectory, True)
        self.assertEqual(pInfo.IsFile, False)
        self.assertEqual(pInfo.IsSymlink, False)

        pInfo = PathInfo(self.testPath +  "/newFile")
        self.assertEqual(pInfo.Exists, False)
        self.assertEqual(pInfo.IsDirectory, False)
        self.assertEqual(pInfo.IsFile, False)
        self.assertEqual(pInfo.IsSymlink, False)

        pInfo.CreateFile()
        self.assertEqual(pInfo.Exists, True)
        self.assertEqual(pInfo.IsDirectory, False)
        self.assertEqual(pInfo.IsFile, True)
        self.assertEqual(pInfo.IsSymlink, False)