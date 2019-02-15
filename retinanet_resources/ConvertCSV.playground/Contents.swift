import Cocoa
import PlaygroundSupport

struct Entry {
    let name: String
    let `class`: String
    let x: String
    let y: String
    let w: String
    let h: String

    init(_ a: [String]) {
        self.name = a[0]
        self.class = a[1]
        self.x = a[2]
        self.y = a[3]
        self.w = a[4]
        self.h = String(a[5].dropLast())
    }

    var tranformed: String {
        let x = Int(self.x)!-Int(w)!/2
        let y = Int(self.y)!-Int(h)!/2
        let x2 = x+Int(w)!
        let y2 = y+Int(h)!
//        return "/Volumes/Rhen/Documents/Developer/MIO-TCD-Localization/train/\(name).jpg,\(x),\(y),\(x2),\(y2),\(self.class)\n"
        return "/home/s3838730/data/ml/dataset/MIO-TCD-Localization/train/\(name).jpg,\(x),\(y),\(x2),\(y2),\(self.class)\n"
    }
}

func process(_ handle: FileHandle) throws {
    let url = Bundle.main.url(forResource: "train", withExtension: "csv")!
    let string = try String(contentsOf: url)
//    var i = 0
    for line in string.components(separatedBy: "\n") {
        let entry = Entry(line.components(separatedBy: ","))
        guard entry.class == "bicycle" else { continue }
        handle.write(entry.tranformed.data(using: .utf8)!)

//        guard i < 10 else { return }
//        i += 1
    }
}

let writeURL = playgroundSharedDataDirectory.appendingPathComponent("out.csv")
let fm = FileManager.default
try? fm.removeItem(at: writeURL)
fm.createFile(atPath: writeURL.path, contents: nil, attributes: nil)

do {
    let handle = try FileHandle(forWritingTo: writeURL)
    try process(handle)
} catch let e {
    print(e)
}
