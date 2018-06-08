var Code = require('code')
var Lab = require('lab')

var isCircular = require('../')

var lab = exports.lab = Lab.script()
var describe = lab.describe
var it = lab.it
var expect = Code.expect

describe('is-circular', function () {
  it('should error if passed a non-object', function (done) {
    expect(isCircular.bind(null, 2)).to.throw(/object/)
    done()
  })

  it('should return true for circular objects', function (done) {
    var x = {}
    x.cyclic = { a: 1, x: x }
    expect(isCircular(x)).to.equal(true)

    done()
  })

  it('should return true for circular objects', function (done) {
    var x = {}
    x.cyclic = { a: {}, x: x }
    expect(isCircular(x)).to.equal(true)

    done()
  })

  it('should return true for circular objects', function (done) {
    var x = {}
    x.cyclic = { a: {}, indirect: { x: x } }
    expect(isCircular(x)).to.equal(true)

    done()
  })

  it('should return false for non-circular objects', function (done) {
    var x = {}
    x.cyclic = { a: 1, b: 2 }
    expect(isCircular(x)).to.equal(false)

    done()
  })

  it('should return false for non-circular objects', function (done) {
    var x = {}
    var y = {}
    x.cyclic = { a: y, b: y }
    expect(isCircular(x)).to.equal(false)

    done()
  })
})
