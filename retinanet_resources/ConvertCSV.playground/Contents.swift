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
        self.h = a[5]
    }

    var tranformed: String {
        return "images/\(name).jpg,\(x),\(y),\(w),\(h),\(self.class)\n"
    }
}

func process(_ handle: FileHandle) throws {
    let url = Bundle.main.url(forResource: "train", withExtension: "csv")!
    let string = try String(contentsOf: url)
//    var out = ""
    for line in string.components(separatedBy: "\n") {
        let entry = Entry(line.components(separatedBy: ","))
//        out.append(entry.tranformed)
        handle.write(entry.tranformed.data(using: .utf8)!)
    }
}

do {
    let writeURL = playgroundSharedDataDirectory.appendingPathComponent("out.csv")
    let handle = try FileHandle(forWritingTo: writeURL)
    try process(handle)
//    try out.write(to: writeURL, atomically: true, encoding: .utf8)
} catch let e {
    print(e)
}
