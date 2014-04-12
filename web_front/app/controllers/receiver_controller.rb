class ReceiverController < ApplicationController
  def photo
  	@user = params[:username]
  	@pass = params[:password]
  	@photo = params[:photo]
  end
end
