require 'test_helper'

class ReceiverControllerTest < ActionController::TestCase
  test "should get photo" do
    get :photo
    assert_response :success
  end

end
